import json

from app.ai.gemini_client import GeminiClient
from app.ai.prompts import RULE_EXTRACTION_PROMPT
from app.models.raw_rules import RawRulesExtraction

from app.utils.logger import logger


class RulesExtractor:

    def __init__(self):
        self.client = GeminiClient()

    def extract_from_text(
        self,
        description: str,
    ) -> RawRulesExtraction:

        logger.info(
            "Rules extraction started"
        )

        prompt = f"""
{RULE_EXTRACTION_PROMPT}

Description:

{description}
"""

        logger.info(
            "Rules prompt generated"
        )

        response = self.client.generate_text(
            prompt
        )

        logger.info(
            "Rules extraction completed"
        )

        logger.info(
            f"Raw Gemini rules response: {response}"
        )

        data = json.loads(
            response
        )

        logger.info(
            "Rules JSON parsed successfully"
        )

        return RawRulesExtraction(
            participants=data.get(
                "participants",
                [],
            ),

            ownership_rules=data.get(
                "ownership_rules",
                [],
            ),

            exclusion_rules=data.get(
                "exclusion_rules",
                [],
            ),

            payments=data.get(
                "payments",
                [],
            ),

            item_quantity_rules=data.get(
                "item_quantity_rules",
                [],
            ),

            shared_remaining_items=data.get(
                "shared_remaining_items",
                False,
            ),

            raw_description=data.get(
                "raw_description",
                description,
            ),
        )