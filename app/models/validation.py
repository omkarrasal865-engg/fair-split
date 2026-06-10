from pydantic import BaseModel

from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules


class ReceiptValidationResult(BaseModel):
    receipt: Receipt

    assumptions: list[str] = []
    flags: list[str] = []


class RulesValidationResult(BaseModel):
    rules: ConsumptionRules

    assumptions: list[str] = []
    flags: list[str] = []