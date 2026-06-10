from app.ai.receipt_extractor import ReceiptExtractor


sample_receipt = """
Brew & Bite Café

Cappuccino            180
Grilled Chicken Sandwich   260
Penne Arrabiata       320
Fresh Lime Soda       120
Brownie               160

Subtotal             1040
Service Charge         52
GST                  54.60
Grand Total          1147
"""


extractor = ReceiptExtractor()

result = extractor.extract_from_text(
    sample_receipt
)

print(result.model_dump_json(indent=2))