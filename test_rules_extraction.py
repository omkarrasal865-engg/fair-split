from app.ai.rules_extractor import RulesExtractor

extractor = RulesExtractor()

description = """
Aman skipped drinks.
Priya and I shared the pasta.
Cheesecake was Karan's.
Priya paid.
"""

result = extractor.extract_from_text(description)

print(result.model_dump())