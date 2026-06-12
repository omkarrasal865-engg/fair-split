from collections import defaultdict

from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules
from app.models.response import PersonBreakdown
from app.services.item_matcher import ItemMatcher


class AllocationEngine:

    def allocate(
        self,
        receipt: Receipt,
        rules: ConsumptionRules
    ) -> list[PersonBreakdown]:

        participants = rules.participants

        item_lists = defaultdict(list)
        subtotals = defaultdict(float)

        exclusion_rules = rules.exclusion_rules

        for item in receipt.items:

            quantity_rules = []

            for quantity_rule in rules.item_quantity_rules:

                if ItemMatcher.matches(
                    quantity_rule.item,
                    item.name,
                ):
                    quantity_rules.append(
                        quantity_rule
                    )

            # V3 Quantity Allocation
            if quantity_rules:

                item_quantity = item.quantity or 1

                if item_quantity <= 0:
                    continue

                unit_price = (
                    item.amount /
                    item_quantity
                )

                allocated_quantity = sum(
                    rule.quantity
                    for rule in quantity_rules
                )

                if allocated_quantity > item_quantity:
                    allocated_quantity = item_quantity

                for rule in quantity_rules:

                    amount = (
                        rule.quantity *
                        unit_price
                    )

                    item_lists[
                        rule.person
                    ].append(
                        f"{item.name} ({rule.quantity})"
                    )

                    subtotals[
                        rule.person
                    ] += amount

                continue

            consumers = None

            # Ownership Rules
            for rule in rules.ownership_rules:

                if ItemMatcher.matches(
                    rule.item,
                    item.name,
                ):
                    consumers = rule.consumers
                    break

            # Default Sharing
            if consumers is None:

                consumers = list(
                    participants
                )

                # Exclusions
                for exclusion in exclusion_rules:

                    if ItemMatcher.matches(
                        exclusion.item,
                        item.name,
                    ):
                        if exclusion.person in consumers:
                            consumers.remove(
                                exclusion.person
                            )

            if not consumers:
                continue

            share = (
                item.amount /
                len(consumers)
            )

            for person in consumers:

                item_lists[
                    person
                ].append(
                    item.name
                )

                subtotals[
                    person
                ] += share

        breakdowns = []

        receipt_subtotal = receipt.subtotal

        for person in participants:

            subtotal = round(
                subtotals[person],
                2,
            )

            if receipt_subtotal > 0:
                ratio = (
                    subtotal /
                    receipt_subtotal
                )
            else:
                ratio = 0

            tax_share = round(
                receipt.tax * ratio,
                2,
            )

            service_share = round(
                receipt.service_charge * ratio,
                2,
            )

            discount_share = round(
                receipt.discount * ratio,
                2,
            )

            total = round(
                subtotal
                + tax_share
                + service_share
                - discount_share,
                2,
            )

            breakdowns.append(
                PersonBreakdown(
                    name=person,
                    items=item_lists[person],
                    subtotal=subtotal,
                    tax_share=tax_share,
                    service_share=service_share,
                    discount_share=discount_share,
                    total=total,
                )
            )

        return breakdowns