import os

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

        self.client = genai.Client(
            api_key=api_key
        )

    def generate_text(
        self,
        prompt: str,
    ) -> str:

        try:

            response = (
                self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt,
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

        except GeminiServiceError:
            raise

        except Exception as e:

            error_message = str(
                e
            ).lower()

            if "429" in error_message:
                raise GeminiServiceError(
                    "Gemini rate limit exceeded"
                )

            if "503" in error_message:
                raise GeminiServiceError(
                    "Gemini service unavailable"
                )

            if "timeout" in error_message:
                raise GeminiServiceError(
                    "Gemini request timed out"
                )

            raise GeminiServiceError(
                f"Gemini request failed: {str(e)}"
            )

    def generate_content(
        self,
        contents,
    ) -> str:

        try:

            response = (
                self.client.models.generate_content(
                    model="gemini-2.5-flash",
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

        except GeminiServiceError:
            raise

        except Exception as e:

            error_message = str(
                e
            ).lower()

            if "429" in error_message:
                raise GeminiServiceError(
                    "Gemini rate limit exceeded"
                )

            if "503" in error_message:
                raise GeminiServiceError(
                    "Gemini service unavailable"
                )

            if "timeout" in error_message:
                raise GeminiServiceError(
                    "Gemini request timed out"
                )

            raise GeminiServiceError(
                f"Gemini request failed: {str(e)}"
            )