from app.models.receipt import (
    Receipt,
    ReceiptItem,
)

from app.models.rules import (
    ConsumptionRules,
    OwnershipRule,
)

from app.services.allocation_engine import (
    AllocationEngine,
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
            consumers=[
                "Priya",
                "User",
            ],
        ),
        OwnershipRule(
            item="Cheesecake",
            consumers=[
                "Karan",
            ],
        ),
    ],
    exclusion_rules=[],
    payments=[],
    assumptions=[],
    flags=[],
)

engine = AllocationEngine()

result = engine.allocate(
    receipt=receipt,
    rules=rules,
)

print("\nALLOCATION RESULT\n")

grand_total = 0

for person in result:
    print(person.model_dump())
    grand_total += person.total

print("\nSUM OF PERSON TOTALS")
print(round(grand_total, 2))