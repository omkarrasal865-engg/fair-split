from app.services.bill_processor import BillProcessor


receipt_text = """
Restaurant: Pasta House

Pasta        320
Pizza        380
Cheesecake   160

Subtotal     860
Tax          86
Service      43
Discount     21.5

Grand Total  967.5
"""

description = """
Priya and I shared the Pasta.
Cheesecake was Karan's.
Priya paid.
"""

processor = BillProcessor()

response = processor.process(
    receipt_text=receipt_text,
    description=description,
)

print(response.model_dump())