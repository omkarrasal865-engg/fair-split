from pydantic import BaseModel


class PersonBreakdown(BaseModel):
    name: str
    items: list[str]

    subtotal: float
    tax_share: float
    service_share: float
    discount_share: float

    total: float


class Reconciliation(BaseModel):
    sum_of_person_totals: float

    grand_total: float

    difference: float

    matches_bill: bool


class Settlement(BaseModel):
    from_person: str
    to_person: str
    amount: float


class UnallocatedItem(BaseModel):
    item: str

    total_quantity: float

    allocated_quantity: float

    remaining_quantity: float

    remaining_amount: float


class FairSplitResponse(BaseModel):
    per_person: list[PersonBreakdown]

    grand_total: float

    reconciliation: Reconciliation

    paid_by: str | None = None

    settle_up: list[Settlement]

    assumptions: list[str]

    flags: list[str]

    unallocated_items: list[UnallocatedItem] = []

    merchant_name: str | None = None

    expense_category: str = "Other"

    insights: list[str] = []