import json

from app.ai.gemini_client import GeminiClient
from app.ai.prompts import RECEIPT_EXTRACTION_PROMPT
from app.models.raw_receipt import RawReceiptExtraction

from app.utils.logger import logger


class ReceiptExtractor:

    def __init__(self):
        self.client = GeminiClient()

    def extract_from_text(
        self,
        receipt_text: str,
    ) -> RawReceiptExtraction:

        logger.info(
            "Receipt extraction started"
        )

        prompt = f"""
{RECEIPT_EXTRACTION_PROMPT}

Receipt Text:

{receipt_text}
"""

        logger.info(
            "Receipt prompt generated"
        )

        response = self.client.generate_text(
            prompt
        )

        logger.info(
            "Receipt extraction completed"
        )

        logger.info(
            f"Raw Gemini receipt response: {response}"
        )

        data = json.loads(
            response
        )

        logger.info(
            "Receipt JSON parsed successfully"
        )

        return RawReceiptExtraction(
            **data
        )