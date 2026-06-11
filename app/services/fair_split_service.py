from app.models.receipt import Receipt
from app.models.rules import ConsumptionRules
from app.models.response import FairSplitResponse

from app.services.allocation_engine import AllocationEngine
from app.services.drift_correction_engine import DriftCorrectionEngine
from app.services.settlement_engine import SettlementEngine
from app.services.reconciliation_engine import ReconciliationEngine


class FairSplitService:

    def __init__(self):
        self.allocation_engine = AllocationEngine()
        self.drift_correction_engine = DriftCorrectionEngine()
        self.settlement_engine = SettlementEngine()
        self.reconciliation_engine = ReconciliationEngine()

    def generate_response(
        self,
        receipt: Receipt,
        rules: ConsumptionRules,
    ) -> FairSplitResponse:

        breakdowns = self.allocation_engine.allocate(
            receipt=receipt,
            rules=rules,
        )

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

        return FairSplitResponse(
            per_person=breakdowns,
            grand_total=receipt.grand_total,
            reconciliation=reconciliation,
            paid_by=paid_by,
            settle_up=settlements,
            assumptions=assumptions,
            flags=flags,
        )