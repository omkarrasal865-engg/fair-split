from pydantic import BaseModel


class OwnershipRule(BaseModel):
    item: str
    consumers: list[str]


class ExclusionRule(BaseModel):
    person: str
    item: str


class PaymentRule(BaseModel):
    person: str
    amount: float | None = None


class ItemQuantityRule(BaseModel):
    item: str
    person: str
    quantity: float


class ConsumptionRules(BaseModel):
    participants: list[str]

    ownership_rules: list[OwnershipRule]

    exclusion_rules: list[ExclusionRule]

    payments: list[PaymentRule]

    item_quantity_rules: list[ItemQuantityRule] = []

    shared_remaining_items: bool = False

    assumptions: list[str] = []

    flags: list[str] = []