"""Microservices for travel booking saga."""

from asimpy import Process, Queue
from typing import Dict, Any
import random


# mccole:flight_service
class FlightService(Process):
    """Microservice for booking flights."""

    def init(self) -> None:
        self.bookings: Dict[str, Dict[str, Any]] = {}
        self.request_queue: Queue = Queue(self._env)
        self.available_seats = 10

        print(f"[{self.now:.1f}] FlightService started (seats: {self.available_seats})")

    async def run(self) -> None:
        """Handle flight booking requests."""
        while True:
            await self.timeout(1.0)

    def book_flight(self, booking_id: str, flight_id: str) -> bool:
        """Book a flight (forward transaction)."""
        print(f"[{self.now:.1f}] FlightService: Booking flight {flight_id}")

        # Simulate occasional failures
        if random.random() < 0.1:
            print(f"[{self.now:.1f}] FlightService: Booking FAILED - system error")
            return False

        if self.available_seats <= 0:
            print(f"[{self.now:.1f}] FlightService: Booking FAILED - no seats")
            return False

        self.available_seats -= 1
        self.bookings[booking_id] = {
            "flight_id": flight_id,
            "status": "booked",
            "seats": 1,
        }

        print(
            f"[{self.now:.1f}] FlightService: ✓ Flight booked "
            f"(remaining: {self.available_seats})"
        )
        return True

    def cancel_flight(self, booking_id: str) -> bool:
        """Cancel flight booking (compensation)."""
        print(f"[{self.now:.1f}] FlightService: COMPENSATING - canceling {booking_id}")

        if booking_id not in self.bookings:
            print(f"[{self.now:.1f}] FlightService: No booking to cancel")
            return True

        seats = self.bookings[booking_id].get("seats", 1)
        self.available_seats += seats
        self.bookings[booking_id]["status"] = "canceled"

        print(
            f"[{self.now:.1f}] FlightService: ✓ Flight canceled "
            f"(available: {self.available_seats})"
        )
        return True
# mccole:/flight_service


# mccole:hotel_service
class HotelService(Process):
    """Microservice for booking hotels."""

    def init(self) -> None:
        self.bookings: Dict[str, Dict[str, Any]] = {}
        self.request_queue: Queue = Queue(self._env)
        self.available_rooms = 5

        print(f"[{self.now:.1f}] HotelService started (rooms: {self.available_rooms})")

    async def run(self) -> None:
        """Handle hotel booking requests."""
        while True:
            await self.timeout(1.0)

    def book_hotel(self, booking_id: str, hotel_id: str) -> bool:
        """Book a hotel (forward transaction)."""
        print(f"[{self.now:.1f}] HotelService: Booking hotel {hotel_id}")

        # Simulate occasional failures
        if random.random() < 0.15:
            print(f"[{self.now:.1f}] HotelService: Booking FAILED - no rooms")
            return False

        if self.available_rooms <= 0:
            print(f"[{self.now:.1f}] HotelService: Booking FAILED - no rooms")
            return False

        self.available_rooms -= 1
        self.bookings[booking_id] = {
            "hotel_id": hotel_id,
            "status": "booked",
            "rooms": 1,
        }

        print(
            f"[{self.now:.1f}] HotelService: ✓ Hotel booked "
            f"(remaining: {self.available_rooms})"
        )
        return True

    def cancel_hotel(self, booking_id: str) -> bool:
        """Cancel hotel booking (compensation)."""
        print(f"[{self.now:.1f}] HotelService: COMPENSATING - canceling {booking_id}")

        if booking_id not in self.bookings:
            print(f"[{self.now:.1f}] HotelService: No booking to cancel")
            return True

        rooms = self.bookings[booking_id].get("rooms", 1)
        self.available_rooms += rooms
        self.bookings[booking_id]["status"] = "canceled"

        print(
            f"[{self.now:.1f}] HotelService: ✓ Hotel canceled "
            f"(available: {self.available_rooms})"
        )
        return True
# mccole:/hotel_service


# mccole:car_service
class CarRentalService(Process):
    """Microservice for renting cars."""

    def init(self) -> None:
        self.bookings: Dict[str, Dict[str, Any]] = {}
        self.request_queue: Queue = Queue(self._env)
        self.available_cars = 3

        print(
            f"[{self.now:.1f}] CarRentalService started (cars: {self.available_cars})"
        )

    async def run(self) -> None:
        """Handle car rental requests."""
        while True:
            await self.timeout(1.0)

    def book_car(self, booking_id: str, car_id: str) -> bool:
        """Book a car (forward transaction)."""
        print(f"[{self.now:.1f}] CarRentalService: Booking car {car_id}")

        # Simulate higher failure rate for demonstration
        if random.random() < 0.3:
            print(f"[{self.now:.1f}] CarRentalService: Booking FAILED - no cars")
            return False

        if self.available_cars <= 0:
            print(f"[{self.now:.1f}] CarRentalService: Booking FAILED - no cars")
            return False

        self.available_cars -= 1
        self.bookings[booking_id] = {"car_id": car_id, "status": "booked", "cars": 1}

        print(
            f"[{self.now:.1f}] CarRentalService: ✓ Car booked "
            f"(remaining: {self.available_cars})"
        )
        return True

    def cancel_car(self, booking_id: str) -> bool:
        """Cancel car rental (compensation)."""
        print(
            f"[{self.now:.1f}] CarRentalService: COMPENSATING - canceling {booking_id}"
        )

        if booking_id not in self.bookings:
            print(f"[{self.now:.1f}] CarRentalService: No booking to cancel")
            return True

        cars = self.bookings[booking_id].get("cars", 1)
        self.available_cars += cars
        self.bookings[booking_id]["status"] = "canceled"

        print(
            f"[{self.now:.1f}] CarRentalService: ✓ Car canceled "
            f"(available: {self.available_cars})"
        )
        return True
# mccole:/car_service
