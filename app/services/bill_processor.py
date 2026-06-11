from app.ai.receipt_extractor import ReceiptExtractor
from app.ai.rules_extractor import RulesExtractor

from app.validators.receipt_validator import ReceiptValidator
from app.validators.rules_validator import RulesValidator

from app.services.fair_split_service import FairSplitService

from app.models.response import FairSplitResponse


class BillProcessor:

    def __init__(self):
        self.receipt_extractor = ReceiptExtractor()
        self.rules_extractor = RulesExtractor()

        self.receipt_validator = ReceiptValidator()
        self.rules_validator = RulesValidator()

        self.fair_split_service = FairSplitService()

    def process(
        self,
        receipt_text: str,
        description: str,
    ) -> FairSplitResponse:

        raw_receipt = self.receipt_extractor.extract_from_text(
            receipt_text
        )

        receipt = self.receipt_validator.validate(
            raw_receipt
        )

        raw_rules = self.rules_extractor.extract_from_text(
            description
        )

        rules = self.rules_validator.validate(
            raw_rules
        )

        return self.fair_split_service.generate_response(
            receipt=receipt,
            rules=rules,
        )