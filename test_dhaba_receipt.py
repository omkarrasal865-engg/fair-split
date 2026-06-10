from app.models.raw_receipt import (
    RawReceiptExtraction,
    RawReceiptItem,
)
from app.validators.receipt_validator import ReceiptValidator


raw_receipt = RawReceiptExtraction(
    restaurant_name="Ganesh Tea Stall",

    items=[
        RawReceiptItem(
            name="Tea",
            quantity=2,
            amount=40,
        ),
        RawReceiptItem(
            name="Poha",
            quantity=1,
            amount=30,
        ),
    ],

    subtotal=None,
    service_charge=None,
    tax=None,
    discount=None,
    grand_total=70,

    raw_text="""
    Tea 40
    Poha 30
    Total 70
    """
)

validator = ReceiptValidator()

result = validator.validate(raw_receipt)

print("\nASSUMPTIONS")
print(result.assumptions)

print("\nFLAGS")
print(result.flags)

print("\nVALIDATED RECEIPT")
print(result.receipt.model_dump())