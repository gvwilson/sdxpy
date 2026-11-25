from dataclasses import dataclass


# mccole:ntpmessage
@dataclass
class NTPMessage:
    """A simplified NTP message packet."""

    # Client timestamps
    t1: float = 0.0  # Client send time
    t2: float = 0.0  # Server receive time
    t3: float = 0.0  # Server transmit time
    t4: float = 0.0  # Client receive time

    # Stratum level (distance from reference clock)
    stratum: int = 0

    def calculate_offset(self) -> float:
        """Calculate clock offset using NTP algorithm.

        offset = ((t2 - t1) + (t3 - t4)) / 2
        """
        if self.t1 and self.t2 and self.t3 and self.t4:
            return ((self.t2 - self.t1) + (self.t3 - self.t4)) / 2.0
        return 0.0

    def calculate_delay(self) -> float:
        """Calculate round-trip delay.

        delay = (t4 - t1) - (t3 - t2)
        """
        if self.t1 and self.t2 and self.t3 and self.t4:
            return (self.t4 - self.t1) - (self.t3 - self.t2)
        return 0.0
# mccole:/ntpmessage
