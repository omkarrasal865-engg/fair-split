import json

from google.genai import types

from app.ai.gemini_client import GeminiClient
from app.ai.prompts import RECEIPT_EXTRACTION_PROMPT
from app.models.raw_receipt import RawReceiptExtraction


class ImageReceiptExtractor:

    def __init__(self):
        self.client = GeminiClient()

    def extract_from_image(
        self,
        image_bytes: bytes,
        mime_type: str,
    ) -> RawReceiptExtraction:

        image_part = types.Part.from_bytes(
            data=image_bytes,
            mime_type=mime_type,
        )

        response = self.client.generate_content(
            contents=[
                RECEIPT_EXTRACTION_PROMPT,
                image_part,
            ]
        )

        print("\n========== IMAGE GEMINI RESPONSE ==========\n")
        print(response)

        data = json.loads(response)

        return RawReceiptExtraction(**data)