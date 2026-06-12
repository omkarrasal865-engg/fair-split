from app.models.receipt import (
    Receipt,
    ReceiptItem,
)

from app.models.rules import (
    ConsumptionRules,
    ItemQuantityRule,
)

from app.services.allocation_engine import (
    AllocationEngine,
)

receipt = Receipt(
    items=[
        ReceiptItem(
            name="Beer",
            quantity=4,
            amount=400,
        ),
    ],
    subtotal=400,
    service_charge=0,
    tax=0,
    discount=0,
    grand_total=400,
)

rules = ConsumptionRules(
    participants=[
        "Aman",
        "Priya",
    ],

    ownership_rules=[],
    exclusion_rules=[],
    payments=[],

    item_quantity_rules=[
        ItemQuantityRule(
            item="Beer",
            person="Aman",
            quantity=3,
        ),
        ItemQuantityRule(
            item="Beer",
            person="Priya",
            quantity=1,
        ),
    ],

    shared_remaining_items=False,
)

engine = AllocationEngine()

result = engine.allocate(
    receipt=receipt,
    rules=rules,
)

for row in result:
    print(row.model_dump())