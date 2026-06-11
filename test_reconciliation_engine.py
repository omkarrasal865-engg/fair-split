from app.models.response import (
    PersonBreakdown,
)

from app.services.reconciliation_engine import (
    ReconciliationEngine,
)


breakdowns = [
    PersonBreakdown(
        name="Priya",
        items=[],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
    PersonBreakdown(
        name="User",
        items=[],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
    PersonBreakdown(
        name="Karan",
        items=[],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
]

engine = ReconciliationEngine()

result = engine.reconcile(
    breakdowns=breakdowns,
    grand_total=967.50,
)

print(result.model_dump())