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

class RawRulesExtraction(BaseModel):
    participants: list[str]

    ownership_rules: list[OwnershipRule]

    exclusion_rules: list[ExclusionRule]

    payments: list[PaymentRule]

    shared_remaining_items: bool = False

    item_quantity_rules: list[ItemQuantityRule] = []

    raw_description: str