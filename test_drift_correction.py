from app.models.response import (
    PersonBreakdown,
)

from app.services.drift_correction_engine import (
    DriftCorrectionEngine,
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

engine = DriftCorrectionEngine()

result = engine.correct(
    breakdowns=breakdowns,
    grand_total=100.00,
)

for row in result:
    print(row.model_dump())

print(
    "\nFINAL TOTAL:",
    round(
        sum(
            person.total
            for person in result
        ),
        2,
    ),
)