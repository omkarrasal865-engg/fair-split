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
            name="Chicken Biryani",
            quantity=1,
            amount=300,
        ),
        ReceiptItem(
            name="Chocolate Brownie",
            quantity=1,
            amount=200,
        ),
    ],
    subtotal=500,
    service_charge=0,
    tax=0,
    discount=0,
    grand_total=500,
)

rules = ConsumptionRules(
    participants=[
        "User",
        "Priya",
    ],

    ownership_rules=[
        OwnershipRule(
            item="Biryani",
            consumers=["User"],
        ),
        OwnershipRule(
            item="Brownie",
            consumers=["Priya"],
        ),
    ],

    exclusion_rules=[],
    payments=[],
    shared_remaining_items=False,
)

engine = AllocationEngine()

result = engine.allocate(
    receipt=receipt,
    rules=rules,
)

for row in result:
    print(row.model_dump())