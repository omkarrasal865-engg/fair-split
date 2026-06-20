from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules
from app.models.response import FairSplitResponse

from app.models.split_result import (
    SplitResult,
)

from app.models.clarification import (
    ClarificationResponse,
    ClarificationQuestion,
)

from app.services.allocation_engine import AllocationEngine

from app.services.quantity_reconciliation_engine import (
    QuantityReconciliationEngine,
)

from app.services.shared_remaining_allocation_engine import (
    SharedRemainingAllocationEngine,
)

from app.services.drift_correction_engine import (
    DriftCorrectionEngine,
)

from app.services.settlement_engine import (
    SettlementEngine,
)

from app.services.reconciliation_engine import (
    ReconciliationEngine,
)

from app.utils.logger import (
    logger,
)


class FairSplitService:

    def __init__(self):
        self.allocation_engine = (
            AllocationEngine()
        )

        self.quantity_reconciliation_engine = (
            QuantityReconciliationEngine()
        )

        self.shared_remaining_allocation_engine = (
            SharedRemainingAllocationEngine()
        )

        self.drift_correction_engine = (
            DriftCorrectionEngine()
        )

        self.settlement_engine = (
            SettlementEngine()
        )

        self.reconciliation_engine = (
            ReconciliationEngine()
        )

    def generate_response(
        self,
        receipt: Receipt,
        rules: ConsumptionRules,
    ) -> SplitResult:

        logger.info(
            "Starting allocation process"
        )

        breakdowns = (
            self.allocation_engine.allocate(
                receipt=receipt,
                rules=rules,
            )
        )

        logger.info(
            "Allocation completed"
        )

        unallocated_items = (
            self.quantity_reconciliation_engine.reconcile(
                receipt=receipt,
                allocation_result=breakdowns,
            )
        )

        if unallocated_items:

            if rules.shared_remaining_items:

                logger.info(
                    f"Shared remainder allocation triggered "
                    f"for {len(unallocated_items)} item(s)"
                )

                breakdowns = (
                    self.shared_remaining_allocation_engine.allocate(
                        breakdowns=breakdowns,
                        unallocated_items=unallocated_items,
                        participant_count=len(
                            rules.participants
                        ),
                    )
                )

                unallocated_items = []

            else:

                logger.info(
                    f"Clarification required for "
                    f"{len(unallocated_items)} item(s)"
                )

                questions = []

                for index, item in enumerate(
                    unallocated_items
                ):

                    questions.append(
                        ClarificationQuestion(
                            id=f"q{index + 1}",
                            type="unallocated_item",
                            item=item.item,
                            remaining_quantity=item.remaining_quantity,
                            remaining_amount=item.remaining_amount,
                            question=(
                                f"Who consumed "
                                f"{item.item}?"
                            ),
                        )
                    )

                return SplitResult(
                    status="needs_clarification",
                    clarification=ClarificationResponse(
                        questions=questions
                    ),
                )

        breakdowns = (
            self.drift_correction_engine.correct(
                breakdowns=breakdowns,
                grand_total=receipt.grand_total,
                allow_correction=True,
            )
        )

        paid_by = None

        if rules.payments:
            paid_by = (
                rules.payments[0].person
            )

        settlements = (
            self.settlement_engine.generate_settlements(
                breakdowns=breakdowns,
                paid_by=paid_by,
            )
        )

        reconciliation = (
            self.reconciliation_engine.reconcile(
                breakdowns=breakdowns,
                grand_total=receipt.grand_total,
            )
        )

        assumptions = list(
            rules.assumptions
        )

        flags = list(
            rules.flags
        )

        logger.info(
            f"Response generated successfully. "
            f"Participants={len(breakdowns)} "
            f"Settlements={len(settlements)}"
        )

        return SplitResult(
            status="completed",
            data=FairSplitResponse(
                per_person=breakdowns,
                grand_total=receipt.grand_total,
                reconciliation=reconciliation,
                paid_by=paid_by,
                settle_up=settlements,
                assumptions=assumptions,
                flags=flags,
                unallocated_items=[],
            ),
        )