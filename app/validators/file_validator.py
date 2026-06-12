from app.exceptions import (
    ValidationError,
)


class FileValidator:

    MAX_FILE_SIZE = (
        10 * 1024 * 1024
    )  # 10 MB

    ALLOWED_TYPES = [
        "image/jpeg",
        "image/png",
        "image/webp",
    ]

    @classmethod
    def validate(
        cls,
        file_type: str,
        file_size: int,
    ):

        if file_type not in cls.ALLOWED_TYPES:
            raise ValidationError(
                "Unsupported image format. Use JPG, PNG or WEBP."
            )

        if file_size == 0:
            raise ValidationError(
                "Uploaded file is empty."
            )

        if (
            file_size
            > cls.MAX_FILE_SIZE
        ):
            raise ValidationError(
                "File exceeds 10 MB limit."
            )