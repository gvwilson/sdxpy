"""Saga orchestrator for coordinating distributed transactions."""

from asimpy import Process, Queue
from typing import Dict
from saga_types import SagaExecution, SagaStatus, SagaStep, BookingRequest
from booking_services import FlightService, HotelService, CarRentalService


# mccole:orch_init
class SagaOrchestrator(Process):
    """Centralized saga coordinator (orchestration pattern)."""

    def init(
        self,
        flight_service: FlightService,
        hotel_service: HotelService,
        car_service: CarRentalService,
    ) -> None:
        self.flight_service = flight_service
        self.hotel_service = hotel_service
        self.car_service = car_service

        self.request_queue: Queue = Queue(self._env)
        self.active_sagas: Dict[str, SagaExecution] = {}

        # Statistics
        self.sagas_completed = 0
        self.sagas_failed = 0

        print(f"[{self.now:.1f}] SagaOrchestrator started\n")

    async def run(self) -> None:
        """Process booking requests."""
        while True:
            request = await self.request_queue.get()
            await self.execute_saga(request)
    # mccole:/orch_init

    # mccole:orch_execute
    async def execute_saga(self, booking: BookingRequest) -> None:
        """Execute travel booking saga."""
        print(f"[{self.now:.1f}] {'=' * 60}")
        print(f"[{self.now:.1f}] Starting saga for {booking}")
        print(f"[{self.now:.1f}] {'=' * 60}")

        # Define saga steps
        steps = [
            SagaStep(
                name="book_flight",
                service_name="FlightService",
                transaction=lambda: self.flight_service.book_flight(
                    booking.booking_id, booking.flight_id
                ),
                compensation=lambda: self.flight_service.cancel_flight(
                    booking.booking_id
                ),
            ),
            SagaStep(
                name="book_hotel",
                service_name="HotelService",
                transaction=lambda: self.hotel_service.book_hotel(
                    booking.booking_id, booking.hotel_id
                ),
                compensation=lambda: self.hotel_service.cancel_hotel(
                    booking.booking_id
                ),
            ),
            SagaStep(
                name="book_car",
                service_name="CarRentalService",
                transaction=lambda: self.car_service.book_car(
                    booking.booking_id, booking.car_id
                ),
                compensation=None,  # Last step doesn't need compensation
            ),
        ]

        saga = SagaExecution(
            saga_id=booking.booking_id, steps=steps, status=SagaStatus.IN_PROGRESS
        )

        self.active_sagas[booking.booking_id] = saga

        # Execute forward transactions
        success = await self.execute_forward(saga)

        if success:
            saga.status = SagaStatus.COMPLETED
            self.sagas_completed += 1
            print(f"\n[{self.now:.1f}] ✓✓✓ Saga {saga.saga_id} COMPLETED ✓✓✓\n")
        else:
            # Execute compensations
            saga.status = SagaStatus.COMPENSATING
            await self.execute_compensation(saga)
            saga.status = SagaStatus.FAILED
            self.sagas_failed += 1
            print(
                f"\n[{self.now:.1f}] ✗✗✗ Saga {saga.saga_id} FAILED - compensated ✗✗✗\n"
            )
    # mccole:/orch_execute

    # mccole:orch_forward
    async def execute_forward(self, saga: SagaExecution) -> bool:
        """Execute forward transactions in sequence."""
        for i, step in enumerate(saga.steps):
            saga.current_step = i

            print(
                f"[{self.now:.1f}] Orchestrator: Executing step {i + 1}/"
                f"{len(saga.steps)}: {step.name}"
            )

            # Simulate network delay
            await self.timeout(0.3)

            # Execute transaction
            success = step.transaction()

            if success:
                saga.completed_steps.append(step.name)
            else:
                saga.failed_step = step.name
                print(f"[{self.now:.1f}] Orchestrator: Step {step.name} FAILED")
                return False

        return True
    # mccole:/orch_forward

    # mccole:orch_compensate
    async def execute_compensation(self, saga: SagaExecution) -> None:
        """Execute compensating transactions in reverse order."""
        print(f"\n[{self.now:.1f}] Orchestrator: Starting compensation...")

        # Compensate in reverse order
        for step_name in reversed(saga.completed_steps):
            # Find the step
            step = next(s for s in saga.steps if s.name == step_name)

            if step.compensation:
                print(f"[{self.now:.1f}] Orchestrator: Compensating {step_name}")

                # Simulate network delay
                await self.timeout(0.2)

                success = step.compensation()

                if not success:
                    print(
                        f"[{self.now:.1f}] Orchestrator: WARNING - "
                        f"Compensation {step_name} failed! Manual intervention needed."
                    )
    # mccole:/orch_compensate
