from pydantic import BaseModel


class ReceiptItem(BaseModel):
    name: str
    quantity: float
    amount: float


class Receipt(BaseModel):
    items: list[ReceiptItem]

    subtotal: float
    service_charge: float
    tax: float
    discount: float

    grand_total: float