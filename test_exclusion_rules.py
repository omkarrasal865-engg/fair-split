from app.models.receipt import (
    Receipt,
    ReceiptItem,
)

from app.models.rules import (
    ConsumptionRules,
    ExclusionRule,
)

from app.services.allocation_engine import (
    AllocationEngine,
)


receipt = Receipt(
    items=[
        ReceiptItem(
            name="Drinks",
            quantity=1,
            amount=300,
        ),
        ReceiptItem(
            name="Pizza",
            quantity=1,
            amount=400,
        ),
    ],
    subtotal=700,
    service_charge=0,
    tax=0,
    discount=0,
    grand_total=700,
)

rules = ConsumptionRules(
    participants=[
        "Aman",
        "Priya",
        "User",
    ],

    ownership_rules=[],

    exclusion_rules=[
        ExclusionRule(
            person="Aman",
            item="Drinks",
        )
    ],

    payments=[],

    shared_remaining_items=True,
)

engine = AllocationEngine()

result = engine.allocate(
    receipt=receipt,
    rules=rules,
)

print("\nEXCLUSION TEST\n")

for row in result:
    print(row.model_dump())