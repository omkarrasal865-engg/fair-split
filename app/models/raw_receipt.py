from pydantic import BaseModel


class RawReceiptItem(BaseModel):
    name: str
    quantity: float | None = None
    amount: float


class RawReceiptExtraction(BaseModel):
    restaurant_name: str | None = None

    items: list[RawReceiptItem]

    subtotal: float | None = None
    service_charge: float | None = None
    tax: float | None = None
    discount: float | None = None
    grand_total: float | None = None

    raw_text: str