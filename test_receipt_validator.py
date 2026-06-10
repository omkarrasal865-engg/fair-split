from app.models.raw_receipt import (
    RawReceiptExtraction,
    RawReceiptItem,
)
from app.validators.receipt_validator import ReceiptValidator


raw_receipt = RawReceiptExtraction(
    restaurant_name="Test Restaurant",
    items=[
        RawReceiptItem(
            name="Pasta",
            quantity=1,
            amount=320,
        ),
        RawReceiptItem(
            name="Pizza",
            quantity=1,
            amount=380,
        ),
        RawReceiptItem(
            name="Brownie",
            quantity=1,
            amount=160,
        ),
    ],

    subtotal=900,   # WRONG ON PURPOSE

    service_charge=45,
    tax=45,
    discount=0,

    grand_total=990,

    raw_text="Test Receipt"
)


validator = ReceiptValidator()

result = validator.validate(raw_receipt)

print("\nASSUMPTIONS")
print(result.assumptions)

print("\nFLAGS")
print(result.flags)

print("\nVALIDATED RECEIPT")
print(result.receipt.model_dump())