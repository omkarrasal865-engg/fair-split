import os
import time

from dotenv import load_dotenv
from google import genai

from app.exceptions import (
    GeminiServiceError,
)

load_dotenv()


class GeminiClient:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:
            raise GeminiServiceError(
                "GEMINI_API_KEY not found"
            )

        print(
            f"GEMINI KEY PREFIX: {api_key[:10]}..."
        )

        self.client = genai.Client(
            api_key=api_key
        )

    def _call_gemini(
        self,
        contents,
    ) -> str:

        max_retries = 4

        for attempt in range(
            max_retries
        ):

            try:

                response = (
                    self.client.models.generate_content(
                        model="gemini-2.5-flash"
                        contents=contents,
                    )
                )

                if (
                    not response
                    or not response.text
                ):
                    raise GeminiServiceError(
                        "Gemini returned empty response"
                    )

                return response.text

            except Exception as e:

                error_message = str(
                    e
                ).lower()

                print(
                    f"\nGEMINI ERROR:\n{e}"
                )

                if (
                    "429" in error_message
                    or "resource_exhausted"
                    in error_message
                ):

                    if (
                        attempt
                        == max_retries - 1
                    ):
                        raise GeminiServiceError(
                            "Gemini rate limit exceeded"
                        )

                    wait_time = (
                        attempt + 1
                    ) * 2

                    print(
                        f"Gemini rate limited. Retrying in {wait_time}s..."
                    )

                    time.sleep(
                        wait_time
                    )

                    continue

                if (
                    "503" in error_message
                    or "unavailable"
                    in error_message
                ):

                    if (
                        attempt
                        == max_retries - 1
                    ):
                        raise GeminiServiceError(
                            "Gemini service unavailable"
                        )

                    wait_time = (
                        attempt + 1
                    ) * 5

                    print(
                        f"Gemini overloaded. Retrying in {wait_time}s..."
                    )

                    time.sleep(
                        wait_time
                    )

                    continue

                if (
                    "timeout"
                    in error_message
                ):
                    raise GeminiServiceError(
                        "Gemini request timed out"
                    )

                raise GeminiServiceError(
                    f"Gemini request failed: {str(e)}"
                )

        raise GeminiServiceError(
            "Gemini unavailable after retries"
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        return self._call_gemini(
            prompt
        )

    def generate_content(
        self,
        contents,
    ) -> str:

        return self._call_gemini(
            contents
        )