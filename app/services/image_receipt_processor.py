from app.ai.image_receipt_extractor import (
    ImageReceiptExtractor,
)

from app.validators.receipt_validator import (
    ReceiptValidator,
)

from app.utils.logger import (
    logger,
)


class ImageReceiptProcessor:

    def __init__(self):
        self.extractor = ImageReceiptExtractor()

        self.validator = ReceiptValidator()

    def process(
        self,
        image_bytes: bytes,
        mime_type: str,
    ):

        logger.info(
            f"Receipt image processing started | mime_type={mime_type}"
        )

        raw_receipt = (
            self.extractor.extract_from_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
            )
        )

        logger.info(
            "Receipt extraction completed"
        )

        validation = (
            self.validator.validate(
                raw_receipt
            )
        )

        logger.info(
            f"Receipt validation completed | items={len(validation.receipt.items)}"
        )

        return validation.receipt