from app.ai.rules_extractor import RulesExtractor

extractor = RulesExtractor()

result = extractor.extract_from_text(
    """
    Aman ate 2 Mutton biriyani and 2 Tandoori Roti.
    Priya ate 1 Mutton biriyani, 2 Tandoori Roti and 1 Chilly chicken.
    Karan ate 1 Mutton biriyani, 1 Tandoori Roti,
    1 Chilly chicken and 2 Chicken pepper.
    Priya paid the bill.
    Share remaining items equally.
    """
)

print(result.model_dump())