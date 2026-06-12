from difflib import SequenceMatcher


class ItemMatcher:

    @staticmethod
    def matches(
        rule_item: str,
        receipt_item: str,
    ) -> bool:

        rule_item = (
            rule_item
            .lower()
            .strip()
        )

        receipt_item = (
            receipt_item
            .lower()
            .strip()
        )

        if rule_item == receipt_item:
            return True

        if rule_item in receipt_item:
            return True

        if receipt_item in rule_item:
            return True

        similarity = SequenceMatcher(
            None,
            rule_item,
            receipt_item,
        ).ratio()

        return similarity >= 0.80