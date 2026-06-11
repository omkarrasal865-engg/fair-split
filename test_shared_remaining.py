from app.models.raw_rules import (
    RawRulesExtraction,
    OwnershipRule,
    PaymentRule,
)

from app.validators.rules_validator import (
    RulesValidator,
)


raw_rules = RawRulesExtraction(
    participants=[
        "User",
        "Priya",
        "Karan",
    ],

    ownership_rules=[
        OwnershipRule(
            item="Pasta",
            consumers=[
                "User",
                "Priya",
            ],
        ),
    ],

    exclusion_rules=[],

    payments=[
        PaymentRule(
            person="Priya",
            amount=None,
        ),
    ],

    shared_remaining_items=True,

    raw_description="""
    Priya and I shared the Pasta.
    Split everything else equally.
    Priya paid.
    """,
)

validator = RulesValidator()

result = validator.validate(
    raw_rules
)

print("\nRULES RESULT\n")

print(result.model_dump())