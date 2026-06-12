from app.ai.receipt_extractor import ReceiptExtractor
from app.ai.rules_extractor import RulesExtractor

from app.validators.receipt_validator import ReceiptValidator
from app.validators.rules_validator import RulesValidator

from app.services.fair_split_service import FairSplitService

from app.models.response import FairSplitResponse

from app.utils.logger import logger


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

        logger.info(
            "Text bill processing started"
        )

        raw_receipt = self.receipt_extractor.extract_from_text(
            receipt_text
        )

        logger.info(
            "Receipt extracted from text"
        )

        receipt_validation = self.receipt_validator.validate(
            raw_receipt
        )

        logger.info(
            f"Receipt validated | items={len(receipt_validation.receipt.items)}"
        )

        raw_rules = self.rules_extractor.extract_from_text(
            description
        )

        logger.info(
            "Consumption rules extracted"
        )

        rules = self.rules_validator.validate(
            raw_rules
        )

        logger.info(
            f"Rules validated | participants={len(rules.participants)}"
        )

        response = self.fair_split_service.generate_response(
            receipt=receipt_validation.receipt,
            rules=rules,
        )

        logger.info(
            "Fair split response generated"
        )

        return response