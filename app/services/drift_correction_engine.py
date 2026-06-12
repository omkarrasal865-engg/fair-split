from app.models.response import (
    PersonBreakdown,
)


class DriftCorrectionEngine:

    def correct(
        self,
        breakdowns: list[PersonBreakdown],
        grand_total: float,
        allow_correction: bool = True,
    ) -> list[PersonBreakdown]:

        if not allow_correction:
            return breakdowns

        current_total = round(
            sum(
                person.total
                for person in breakdowns
            ),
            2,
        )

        difference = round(
            grand_total - current_total,
            2,
        )

        if difference == 0:
            return breakdowns

        largest_person = max(
            breakdowns,
            key=lambda person: person.total,
        )

        largest_person.total = round(
            largest_person.total + difference,
            2,
        )

        return breakdowns