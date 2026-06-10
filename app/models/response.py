from pydantic import BaseModel


class PersonBreakdown(BaseModel):
    name: str
    items: list[str]

    subtotal: int
    tax_share: int
    service_share: int
    discount_share: int

    total: int


class Reconciliation(BaseModel):
    sum_of_person_totals: int
    matches_bill: bool


class Settlement(BaseModel):
    from_person: str
    to_person: str
    amount: int


class FairSplitResponse(BaseModel):
    per_person: list[PersonBreakdown]

    grand_total: int

    reconciliation: Reconciliation

    paid_by: str | None = None

    settle_up: list[Settlement]

    assumptions: list[str]
    flags: list[str]