from app.ai.image_receipt_extractor import (
    ImageReceiptExtractor,
)

from app.validators.receipt_validator import (
    ReceiptValidator,
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

        raw_receipt = (
            self.extractor.extract_from_image(
                image_bytes=image_bytes,
                mime_type=mime_type,
            )
        )

        validation = (
            self.validator.validate(
                raw_receipt
            )
        )

        return validation.receipt