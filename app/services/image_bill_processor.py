from app.ai.image_receipt_extractor import (
    ImageReceiptExtractor,
)

from app.ai.rules_extractor import (
    RulesExtractor,
)

from app.validators.receipt_validator import (
    ReceiptValidator,
)

from app.validators.rules_validator import (
    RulesValidator,
)

from app.services.fair_split_service import (
    FairSplitService,
)

from app.services.session_store import (
    SessionStore,
)

from app.models.split_result import (
    SplitResult,
)

from app.utils.logger import (
    logger,
)


class ImageBillProcessor:

    def __init__(self):

        self.receipt_extractor = (
            ImageReceiptExtractor()
        )

        self.rules_extractor = (
            RulesExtractor()
        )

        self.receipt_validator = (
            ReceiptValidator()
        )

        self.rules_validator = (
            RulesValidator()
        )

        self.fair_split_service = (
            FairSplitService()
        )

    def process(
        self,
        image_bytes: bytes,
        mime_type: str,
        description: str,
    ) -> SplitResult:

        logger.info(
            "Image bill processing started"
        )

        raw_receipt = (
            self.receipt_extractor.extract_from_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
            )
        )

        logger.info(
            "Receipt extracted from image"
        )

        receipt_validation = (
            self.receipt_validator.validate(
                raw_receipt
            )
        )

        logger.info(
            f"Receipt validated | items={len(receipt_validation.receipt.items)}"
        )

        raw_rules = (
            self.rules_extractor.extract_from_text(
                description
            )
        )

        logger.info(
            "Consumption rules extracted"
        )

        rules = (
            self.rules_validator.validate(
                raw_rules
            )
        )

        logger.info(
            f"Rules validated | participants={len(rules.participants)}"
        )

        response = (
            self.fair_split_service.generate_response(
                receipt=receipt_validation.receipt,
                rules=rules,
            )
        )

        # Save clarification session
        if (
            response.status
            == "needs_clarification"
        ):

            session_id = (
                SessionStore.create(
                    receipt=receipt_validation.receipt,
                    rules=rules,
                    unallocated_items=(
                        response.clarification.questions
                    ),
                )
            )

            response.session_id = (
                session_id
            )

            logger.info(
                f"Clarification session created | session_id={session_id}"
            )

        logger.info(
            f"Processing completed with status={response.status}"
        )

        return response