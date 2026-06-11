from app.models.response import (
    PersonBreakdown,
)

from app.services.settlement_engine import (
    SettlementEngine,
)


breakdowns = [
    PersonBreakdown(
        name="Priya",
        items=["Pasta", "Pizza"],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
    PersonBreakdown(
        name="User",
        items=["Pasta", "Pizza"],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
    PersonBreakdown(
        name="Karan",
        items=["Pizza", "Cheesecake"],
        subtotal=286.67,
        tax_share=28.67,
        service_share=14.33,
        discount_share=7.17,
        total=322.50,
    ),
]

engine = SettlementEngine()

settlements = engine.generate_settlements(
    breakdowns=breakdowns,
    paid_by="Priya",
)

print("\nSETTLEMENTS\n")

for settlement in settlements:
    print(settlement.model_dump())