from dataclasses import dataclass


@dataclass
class UnallocatedQuantity:
    item: str
    total_quantity: float
    allocated_quantity: float
    remaining_quantity: float
    remaining_amount: float