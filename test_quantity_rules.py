from app.models.raw_rules import (
    RawRulesExtraction,
    ItemQuantityRule,
)

from app.validators.rules_validator import (
    RulesValidator,
)

raw_rules = RawRulesExtraction(
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

    raw_description=""
)

validator = RulesValidator()

result = validator.validate(
    raw_rules
)

print(result.model_dump())