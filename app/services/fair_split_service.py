from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules
from app.models.response import FairSplitResponse

from app.services.allocation_engine import AllocationEngine
from app.services.quantity_reconciliation_engine import (
    QuantityReconciliationEngine,
)
from app.services.drift_correction_engine import DriftCorrectionEngine
from app.services.settlement_engine import SettlementEngine
from app.services.reconciliation_engine import ReconciliationEngine


class FairSplitService:

    def __init__(self):
        self.allocation_engine = AllocationEngine()

        self.quantity_reconciliation_engine = (
            QuantityReconciliationEngine()
        )

        self.drift_correction_engine = (
            DriftCorrectionEngine()
        )

        self.settlement_engine = SettlementEngine()

        self.reconciliation_engine = (
            ReconciliationEngine()
        )

    def generate_response(
        self,
        receipt: Receipt,
        rules: ConsumptionRules,
    ) -> FairSplitResponse:

        breakdowns = self.allocation_engine.allocate(
            receipt=receipt,
            rules=rules,
        )

        unallocated_items = (
            self.quantity_reconciliation_engine.reconcile(
                receipt=receipt,
                allocation_result=breakdowns,
            )
        )

        response_unallocated_items = [
            {
                "item": item.item,
                "total_quantity": item.total_quantity,
                "allocated_quantity": item.allocated_quantity,
                "remaining_quantity": item.remaining_quantity,
                "remaining_amount": item.remaining_amount,
            }
            for item in unallocated_items
        ]

        breakdowns = self.drift_correction_engine.correct(
            breakdowns=breakdowns,
            grand_total=receipt.grand_total,
        )

        paid_by = None

        if rules.payments:
            paid_by = rules.payments[0].person

        settlements = self.settlement_engine.generate_settlements(
            breakdowns=breakdowns,
            paid_by=paid_by,
        )

        reconciliation = self.reconciliation_engine.reconcile(
            breakdowns=breakdowns,
            grand_total=receipt.grand_total,
        )

        assumptions = list(rules.assumptions)

        flags = list(rules.flags)

        if unallocated_items:
            flags.append(
                "Receipt contains quantities that were not allocated."
            )

        return FairSplitResponse(
            per_person=breakdowns,
            grand_total=receipt.grand_total,
            reconciliation=reconciliation,
            paid_by=paid_by,
            settle_up=settlements,
            assumptions=assumptions,
            flags=flags,
            unallocated_items=response_unallocated_items,
        )