import json

from app.ai.gemini_client import GeminiClient
from app.ai.prompts import RULE_EXTRACTION_PROMPT
from app.models.raw_rules import RawRulesExtraction


class RulesExtractor:
    def __init__(self):
        self.client = GeminiClient()

    def extract_from_text(
        self,
        description: str
    ) -> RawRulesExtraction:

        prompt = f"""
{RULE_EXTRACTION_PROMPT}

Description:

{description}
"""

        response = self.client.generate_text(prompt)

        data = json.loads(response)

        return RawRulesExtraction(**data)