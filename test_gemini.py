from app.ai.gemini_client import GeminiClient


client = GeminiClient()

response = client.generate_text(
    "Reply with exactly: Gemini connection successful"
)

print(response)