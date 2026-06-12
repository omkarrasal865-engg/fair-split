from app.models.response import (
    PersonBreakdown,
)


class SharedRemainingAllocationEngine:

    def allocate(
        self,
        breakdowns: list[PersonBreakdown],
        unallocated_items,
        participant_count: int,
    ) -> list[PersonBreakdown]:

        if participant_count == 0:
            return breakdowns

        for item in unallocated_items:

            share_amount = round(
                item.remaining_amount / participant_count,
                2,
            )

            for person in breakdowns:

                person.items.append(
                    f"{item.item} (shared remainder)"
                )

                person.subtotal = round(
                    person.subtotal + share_amount,
                    2,
                )

                person.total = round(
                   person.total + share_amount,
                   2,
)

        return breakdowns