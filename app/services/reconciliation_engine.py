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

        difference = round(
            grand_total
            - sum_of_person_totals,
            2,
        )

        matches_bill = (
            difference == 0
        )

        return Reconciliation(
            sum_of_person_totals=
                sum_of_person_totals,

            grand_total=
                grand_total,

            difference=
                difference,

            matches_bill=
                matches_bill,
        )