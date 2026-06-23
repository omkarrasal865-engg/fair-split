class InsightEngine:

    def generate(
        self,
        receipt,
        breakdowns,
    ) -> list[str]:

        insights = []

        if not breakdowns:
            return insights

        highest_spender = max(
            breakdowns,
            key=lambda person: person.total,
        )

        insights.append(
            f"{highest_spender.name} spent the most (₹{round(highest_spender.total, 2)})."
        )

        highest_item = max(
            receipt.items,
            key=lambda item: item.amount,
        )

        contribution = round(
            (
                highest_item.amount
                / receipt.grand_total
            )
            * 100,
            1,
        )

        insights.append(
            f"{highest_item.name} contributed {contribution}% of the bill."
        )

        if receipt.tax > 0:

            tax_percent = round(
                (
                    receipt.tax
                    / receipt.subtotal
                )
                * 100,
                2,
            )

            insights.append(
                f"Tax rate was approximately {tax_percent}%."
            )

        return insights