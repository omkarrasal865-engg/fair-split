from app.models.raw_rules import (
    RawRulesExtraction,
    OwnershipRule,
    ExclusionRule,
    PaymentRule,
)

from app.validators.rules_validator import RulesValidator


raw_rules = RawRulesExtraction(
    participants=[
        "Aman",
        "Priya",
        "User",
        "Karan",
    ],
    ownership_rules=[
        OwnershipRule(
            item="pasta",
            consumers=["Priya", "User"]
        ),
        OwnershipRule(
            item="Cheesecake",
            consumers=["Karan"]
        )
    ],
    exclusion_rules=[
        ExclusionRule(
            person="Aman",
            item="drinks"
        )
    ],
    payments=[
        PaymentRule(
            person="Priya"
        )
    ],
    raw_description="""
    Aman skipped drinks.
    Priya and I shared the pasta.
    Cheesecake was Karan's.
    Priya paid.
    """
)

validator = RulesValidator()

result = validator.validate(raw_rules)

print("\nASSUMPTIONS")
print(result.assumptions)

print("\nFLAGS")
print(result.flags)

print("\nVALIDATED RULES")
print(result.model_dump())