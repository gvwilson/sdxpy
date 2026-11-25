"""Choreography-based saga implementation.

In choreography, there is no central orchestrator.
Instead, each service publishes events when it completes or fails a step,
and other services listen for those events and decide what to do next.

Comparison with orchestration:
  Orchestration:  one process (orchestrator) drives all steps explicitly.
                  Easy to trace, easy to add timeouts, single point of failure.
  Choreography:  each service reacts to events from other services.
                  No single point of failure, more decentralized,
                  but harder to follow the overall flow and harder to debug.

Compensation ordering:
  Whether using orchestration or choreography, compensating transactions MUST run
  in the reverse order of the forward transactions.  If we booked flight → hotel → car,
  and car booking failed, we must cancel hotel BEFORE cancelling flight.
  Reversing the order ensures we don't leave the system in a partial state
  where a compensation for step N has been applied but the resource from step N-1
  is still committed.  In choreography, this ordering is enforced by the event chain:
  the car service publishes "car_failed", which triggers hotel compensation,
  which publishes "hotel_compensated", which triggers flight compensation.
"""

from asimpy import Process, Queue
from saga_types import SagaEvent
from booking_services import FlightService, HotelService, CarRentalService
from typing import Dict, List


# mccole:event_bus
class EventBus(Process):
    """Simple pub-sub event bus for choreography.

    Services publish events to named topics.
    Other services subscribe to topics and receive events.
    """

    def init(self) -> None:
        self.subscriptions: Dict[str, List[Queue]] = {}
        self.events_published = 0

    async def run(self) -> None:
        """Event bus has no run loop; it is used directly via publish/subscribe."""
        while True:
            await self.timeout(9999)

    def subscribe(self, event_type: str, queue: Queue) -> None:
        """Subscribe queue to receive events of a given type."""
        if event_type not in self.subscriptions:
            self.subscriptions[event_type] = []
        self.subscriptions[event_type].append(queue)

    async def publish(self, event: SagaEvent) -> None:
        """Publish an event to all subscribers."""
        self.events_published += 1
        print(f"[{self.now:.1f}] EventBus: {event}")
        subscribers = self.subscriptions.get(event.event_type, [])
        for q in subscribers:
            await q.put(event)
# mccole:/event_bus


# mccole:choreographed_flight
class ChoreographedFlightService(Process):
    """Flight service driven by events rather than direct calls.

    Listens for "booking_started" events, tries to book a flight,
    then publishes "flight_booked" or "flight_booking_failed".
    On compensation, listens for "hotel_compensated" and cancels the flight.
    """

    def init(
        self,
        bus: EventBus,
        flight_service: FlightService,
    ) -> None:
        self.bus = bus
        self.flight_service = flight_service
        self.inbox: Queue = Queue(self._env)
        self.compensate_inbox: Queue = Queue(self._env)

        # Subscribe to relevant events.
        bus.subscribe("booking_started", self.inbox)
        bus.subscribe("hotel_compensated", self.compensate_inbox)

    async def run(self) -> None:
        """Process events concurrently: forward bookings and compensations."""
        while True:
            # Wait for either a new booking or a compensation request.
            from asimpy import FirstOf
            trigger = FirstOf(
                self._env,
                self.inbox.get(),
                self.compensate_inbox.get(),
            )
            event = await trigger

            if event.event_type == "booking_started":
                await self._handle_booking(event)
            elif event.event_type == "hotel_compensated":
                await self._handle_compensation(event)

    async def _handle_booking(self, event: SagaEvent) -> None:
        booking_id = event.data["booking_id"]
        flight_id = event.data["flight_id"]
        await self.bus.timeout(0.3)  # simulate network delay
        success = self.flight_service.book_flight(booking_id, flight_id)
        if success:
            await self.bus.publish(SagaEvent(
                event_type="flight_booked",
                saga_id=event.saga_id,
                data={"booking_id": booking_id, "flight_id": flight_id},
            ))
        else:
            await self.bus.publish(SagaEvent(
                event_type="flight_booking_failed",
                saga_id=event.saga_id,
                data={"booking_id": booking_id},
            ))

    async def _handle_compensation(self, event: SagaEvent) -> None:
        booking_id = event.data["booking_id"]
        await self.bus.timeout(0.2)
        self.flight_service.cancel_flight(booking_id)
        await self.bus.publish(SagaEvent(
            event_type="flight_compensated",
            saga_id=event.saga_id,
            data={"booking_id": booking_id},
        ))
# mccole:/choreographed_flight


# mccole:choreographed_hotel
class ChoreographedHotelService(Process):
    """Hotel service driven by events.

    Listens for "flight_booked", tries to book a hotel, and publishes
    "hotel_booked" or "hotel_booking_failed".
    Compensation is triggered by "car_booking_failed".
    """

    def init(self, bus: EventBus, hotel_service: HotelService) -> None:
        self.bus = bus
        self.hotel_service = hotel_service
        self.inbox: Queue = Queue(self._env)
        self.compensate_inbox: Queue = Queue(self._env)
        bus.subscribe("flight_booked", self.inbox)
        bus.subscribe("car_booking_failed", self.compensate_inbox)

    async def run(self) -> None:
        from asimpy import FirstOf
        while True:
            trigger = FirstOf(
                self._env,
                self.inbox.get(),
                self.compensate_inbox.get(),
            )
            event = await trigger
            if event.event_type == "flight_booked":
                await self._handle_booking(event)
            elif event.event_type == "car_booking_failed":
                await self._handle_compensation(event)

    async def _handle_booking(self, event: SagaEvent) -> None:
        booking_id = event.data["booking_id"]
        hotel_id = event.data.get("hotel_id", "hotel-1")
        await self.bus.timeout(0.3)
        success = self.hotel_service.book_hotel(booking_id, hotel_id)
        if success:
            await self.bus.publish(SagaEvent(
                event_type="hotel_booked",
                saga_id=event.saga_id,
                data={"booking_id": booking_id},
            ))
        else:
            await self.bus.publish(SagaEvent(
                event_type="hotel_booking_failed",
                saga_id=event.saga_id,
                data={"booking_id": booking_id},
            ))

    async def _handle_compensation(self, event: SagaEvent) -> None:
        # Compensations run in reverse order: car failed, so cancel hotel first.
        booking_id = event.data["booking_id"]
        await self.bus.timeout(0.2)
        self.hotel_service.cancel_hotel(booking_id)
        await self.bus.publish(SagaEvent(
            event_type="hotel_compensated",
            saga_id=event.saga_id,
            data={"booking_id": booking_id},
        ))
# mccole:/choreographed_hotel


# mccole:choreographed_car
class ChoreographedCarService(Process):
    """Car rental service driven by events.

    Listens for "hotel_booked" and publishes "car_booked" or "car_booking_failed".
    Car is the last step, so it initiates compensation when it fails.
    """

    def init(self, bus: EventBus, car_service: CarRentalService) -> None:
        self.bus = bus
        self.car_service = car_service
        self.inbox: Queue = Queue(self._env)
        bus.subscribe("hotel_booked", self.inbox)

    async def run(self) -> None:
        while True:
            event = await self.inbox.get()
            await self._handle_booking(event)

    async def _handle_booking(self, event: SagaEvent) -> None:
        booking_id = event.data["booking_id"]
        car_id = event.data.get("car_id", "car-1")
        await self.bus.timeout(0.3)
        success = self.car_service.book_car(booking_id, car_id)
        if success:
            await self.bus.publish(SagaEvent(
                event_type="car_booked",
                saga_id=event.saga_id,
                data={"booking_id": booking_id},
            ))
        else:
            # Car is the last step; trigger compensation chain in reverse.
            await self.bus.publish(SagaEvent(
                event_type="car_booking_failed",
                saga_id=event.saga_id,
                data={"booking_id": booking_id},
            ))
# mccole:/choreographed_car
