from app.models.receipt import (
    Receipt,
    ReceiptItem,
)

from app.models.rules import (
    ConsumptionRules,
    OwnershipRule,
    PaymentRule,
)

from app.services.fair_split_service import (
    FairSplitService,
)


receipt = Receipt(
    items=[
        ReceiptItem(
            name="Pasta",
            quantity=1,
            amount=320,
        ),
        ReceiptItem(
            name="Pizza",
            quantity=1,
            amount=380,
        ),
        ReceiptItem(
            name="Cheesecake",
            quantity=1,
            amount=160,
        ),
    ],
    subtotal=860,
    service_charge=43,
    tax=86,
    discount=21.5,
    grand_total=967.5,
)

rules = ConsumptionRules(
    participants=[
        "Priya",
        "User",
        "Karan",
    ],
    ownership_rules=[
        OwnershipRule(
            item="Pasta",
            consumers=["Priya", "User"],
        ),
        OwnershipRule(
            item="Cheesecake",
            consumers=["Karan"],
        ),
    ],
    exclusion_rules=[],
    payments=[
        PaymentRule(
            person="Priya",
        )
    ],
    assumptions=[],
    flags=[],
)

service = FairSplitService()

response = service.generate_response(
    receipt=receipt,
    rules=rules,
)

print(response.model_dump())