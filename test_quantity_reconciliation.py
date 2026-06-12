from app.models.receipt import ReceiptItem, Receipt
from app.services.quantity_reconciliation_engine import (
    QuantityReconciliationEngine
)


def test_remaining_quantity_detected():

    receipt = Receipt(
        items=[
            ReceiptItem(
                name="Beer",
                quantity=4,
                price=400,
            )
        ],
        subtotal=400,
        tax=0,
        service_charge=0,
        discount=0,
        total=400,
    )

    allocation_result = [
        {
            "name": "Aman",
            "items": ["Beer (2.0)"],
        }
    ]

    result = (
        QuantityReconciliationEngine()
        .reconcile(
            receipt,
            allocation_result,
        )
    )

    assert len(result) == 1

    assert result[0].item == "Beer"

    assert result[0].remaining_quantity == 2

    assert result[0].remaining_amount == 200