from app.models.receipt import Receipt, ReceiptItem
from app.models.rules import (
    ConsumptionRules,
    ItemQuantityRule,
)
from app.services.fair_split_service import FairSplitService


receipt = Receipt(
    items=[
        ReceiptItem(
            name="Beer",
            quantity=4,
            amount=400,
        )
    ],
    subtotal=400,
    service_charge=0,
    tax=0,
    discount=0,
    grand_total=400,
)

rules = ConsumptionRules(
    participants=["Aman"],

    ownership_rules=[],

    exclusion_rules=[],

    payments=[],

    item_quantity_rules=[
        ItemQuantityRule(
            item="Beer",
            person="Aman",
            quantity=2,
        )
    ],

    shared_remaining_items=False,

    assumptions=[],

    flags=[],
)

service = FairSplitService()

response = service.generate_response(
    receipt=receipt,
    rules=rules,
)

print(response.model_dump())