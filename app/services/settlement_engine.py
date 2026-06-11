from app.models.response import (
    PersonBreakdown,
    Settlement,
)


class SettlementEngine:

    def generate_settlements(
        self,
        breakdowns: list[PersonBreakdown],
        paid_by: str | None,
    ) -> list[Settlement]:

        if not paid_by:
            return []

        settlements = []

        for person in breakdowns:

            if person.name == paid_by:
                continue

            settlements.append(
                Settlement(
                    from_person=person.name,
                    to_person=paid_by,
                    amount=round(person.total, 2),
                )
            )

        return settlements