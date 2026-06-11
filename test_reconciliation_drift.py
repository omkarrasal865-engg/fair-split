from app.models.response import (
    PersonBreakdown,
)

from app.services.reconciliation_engine import (
    ReconciliationEngine,
)


breakdowns = [
    PersonBreakdown(
        name="A",
        items=[],
        subtotal=0,
        tax_share=0,
        service_share=0,
        discount_share=0,
        total=33.33,
    ),
    PersonBreakdown(
        name="B",
        items=[],
        subtotal=0,
        tax_share=0,
        service_share=0,
        discount_share=0,
        total=33.33,
    ),
    PersonBreakdown(
        name="C",
        items=[],
        subtotal=0,
        tax_share=0,
        service_share=0,
        discount_share=0,
        total=33.33,
    ),
]

engine = ReconciliationEngine()

result = engine.reconcile(
    breakdowns=breakdowns,
    grand_total=100.00,
)

print(result.model_dump())