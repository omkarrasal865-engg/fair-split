from app.models.response import (
    PersonBreakdown,
    Reconciliation,
)


class ReconciliationEngine:

    def reconcile(
        self,
        breakdowns: list[PersonBreakdown],
        grand_total: float,
    ) -> Reconciliation:

        sum_of_person_totals = round(
            sum(
                person.total
                for person in breakdowns
            ),
            2,
        )

        difference = abs(
            sum_of_person_totals
            - grand_total
        )

        matches_bill = difference <= 0.05

        return Reconciliation(
            sum_of_person_totals=sum_of_person_totals,
            matches_bill=matches_bill,
        )