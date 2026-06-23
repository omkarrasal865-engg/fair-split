from app.models.rules import (
    ItemQuantityRule,
)

from app.services.session_store import (
    SessionStore,
)

from app.services.fair_split_service import (
    FairSplitService,
)


class ClarificationService:

    def __init__(self):
        self.fair_split_service = (
            FairSplitService()
        )

    def process(
        self,
        session_id: str,
        clarification_request,
    ):

        session = (
            SessionStore.get(
                session_id
            )
        )

        if not session:
            raise ValueError(
                "Session not found"
            )

        receipt = session["receipt"]

        rules = session["rules"]

        for answer in (
            clarification_request.answers
        ):

            for consumer in (
                answer.consumers
            ):

                rules.item_quantity_rules.append(
                    ItemQuantityRule(
                        item=answer.item,
                        person=consumer.person,
                        quantity=consumer.quantity,
                    )
                )

        SessionStore.delete(
            session_id
        )

        return (
            self.fair_split_service.generate_response(
                receipt=receipt,
                rules=rules,
            )
        )