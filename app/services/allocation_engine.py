from collections import defaultdict

from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules
from app.models.response import PersonBreakdown


class AllocationEngine:

    def allocate(
        self,
        receipt: Receipt,
        rules: ConsumptionRules
    ) -> list[PersonBreakdown]:

        participants = rules.participants

        item_lists = defaultdict(list)
        subtotals = defaultdict(float)

        ownership_lookup = {}

        for rule in rules.ownership_rules:
            ownership_lookup[rule.item.lower()] = rule.consumers

        for item in receipt.items:

            consumers = ownership_lookup.get(
                item.name.lower()
            )

            if consumers is None:
                consumers = participants

            share = item.amount / len(consumers)

            for person in consumers:
                item_lists[person].append(item.name)
                subtotals[person] += share

        breakdowns = []

        receipt_subtotal = receipt.subtotal

        for person in participants:

            subtotal = round(subtotals[person], 2)

            if receipt_subtotal > 0:
                ratio = subtotal / receipt_subtotal
            else:
                ratio = 0

            tax_share = round(
                receipt.tax * ratio,
                2
            )

            service_share = round(
                receipt.service_charge * ratio,
                2
            )

            discount_share = round(
                receipt.discount * ratio,
                2
            )

            total = round(
                subtotal
                + tax_share
                + service_share
                - discount_share,
                2
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