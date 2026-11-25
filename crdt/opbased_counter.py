"""Operation-based PN-Counter (CmRDT)."""

from dataclasses import dataclass


# mccole:op
@dataclass
class Operation:
    """An operation on a CRDT."""

    op_type: str
    replica_id: str
    amount: int = 0


# mccole:/op


# mccole:counter
class OpBasedCounter:
    """Operation-based PN-Counter."""

    def __init__(self, replica_id: str):
        self.replica_id = replica_id
        self.value = 0
        self.applied_ops: set[str] = set()  # For deduplication

    def increment(self, amount: int = 1) -> Operation:
        """Create increment operation."""
        return Operation(op_type="increment", replica_id=self.replica_id, amount=amount)

    def decrement(self, amount: int = 1) -> Operation:
        """Create decrement operation."""
        return Operation(op_type="decrement", replica_id=self.replica_id, amount=amount)

    def apply(self, op: Operation, op_id: str):
        """Apply an operation if not already applied."""
        if op_id in self.applied_ops:
            return  # Already applied, skip (idempotence)

        self.applied_ops.add(op_id)

        if op.op_type == "increment":
            self.value += op.amount
        elif op.op_type == "decrement":
            self.value -= op.amount

    # mccole:/counter

    def __str__(self):
        return f"OpCounter(id={self.replica_id}, value={self.value})"
