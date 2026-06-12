from pathlib import Path

from app.ai.image_receipt_extractor import (
    ImageReceiptExtractor,
)


image_path = Path("1st reciept 3150.jpg")

image_bytes = image_path.read_bytes()

extractor = ImageReceiptExtractor()

result = extractor.extract_from_image(
    image_bytes=image_bytes,
    mime_type="image/jpeg",
)

print(result.model_dump())