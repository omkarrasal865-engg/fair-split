import json

from app.ai.gemini_client import GeminiClient
from app.ai.prompts import RECEIPT_EXTRACTION_PROMPT
from app.models.raw_receipt import RawReceiptExtraction


class ReceiptExtractor:
    def __init__(self):
        self.client = GeminiClient()

    def extract_from_text(
        self,
        receipt_text: str
    ) -> RawReceiptExtraction:

        prompt = f"""
{RECEIPT_EXTRACTION_PROMPT}

Receipt Text:

{receipt_text}
"""

        response = self.client.generate_text(prompt)

        data = json.loads(response)

        return RawReceiptExtraction(**data)