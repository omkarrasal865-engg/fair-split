from pydantic import BaseModel


class AllocationRule(BaseModel):
    item: str
    consumers: list[str]


class ConsumptionRules(BaseModel):
    people: list[str]
    allocations: list[AllocationRule]

    paid_by: str | None = None