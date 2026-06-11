from app.services.item_matcher import (
    ItemMatcher,
)

tests = [
    ("biryani", "Chicken Biryani"),
    ("brownie", "Chocolate Brownie"),
    ("fried rice", "Veg Fried Rice"),
    ("cola", "Coca Cola"),
    ("pizza", "Pizza"),
]

for rule_item, receipt_item in tests:

    result = ItemMatcher.matches(
        rule_item,
        receipt_item,
    )

    print(
        f"{rule_item} -> {receipt_item} = {result}"
    )