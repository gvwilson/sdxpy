"""Demonstration of orchestration-based Saga pattern."""

from asimpy import Environment, Process
from saga_orchestrator import SagaOrchestrator
from booking_services import FlightService, HotelService, CarRentalService
from saga_types import BookingRequest
from dsdx import dsdx


# mccole:orchestratedexample
def main():
    env = Environment()

    # Create services
    flight_service = FlightService(env)
    hotel_service = HotelService(env)
    car_service = CarRentalService(env)

    # Create orchestrator
    orchestrator = SagaOrchestrator(env, flight_service, hotel_service, car_service)

    # Submit booking requests
    class BookingGenerator(Process):
        def init(self, orch: SagaOrchestrator) -> None:
            self.orch = orch

        async def run(self) -> None:
            for i in range(5):
                booking = BookingRequest(
                    booking_id=f"BOOK{i + 1:03d}",
                    customer_id=f"CUST{i + 1}",
                    flight_id="FL123",
                    hotel_id="HTL456",
                    car_id="CAR789",
                )

                await self.orch.request_queue.put(booking)
                await self.timeout(3.0)

    BookingGenerator(env, orchestrator)

    # Run simulation
    env.run(until=40)

    # Print summary
    print("\n" + "=" * 60)
    print("Final State:")
    print("=" * 60)
    print(f"Flight seats available: {flight_service.available_seats}/10")
    print(f"Hotel rooms available: {hotel_service.available_rooms}/5")
    print(f"Cars available: {car_service.available_cars}/3")
    print(f"\nCompleted sagas: {orchestrator.sagas_completed}")
    print(f"Failed sagas: {orchestrator.sagas_failed}")
# mccole:/orchestratedexample


if __name__ == "__main__":
    dsdx(main)
