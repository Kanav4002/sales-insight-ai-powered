import logging
import re
from fastapi import HTTPException, UploadFile, status
from pydantic import EmailStr, ValidationError

logger = logging.getLogger(__name__)

ALLOWED_EXTENSIONS = {"csv", "xlsx"}


def validate_file_upload(file: UploadFile) -> None:
    filename = (file.filename or "").strip()
    if not filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    if "." not in filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File must have an extension (.csv or .xlsx)",
        )

    ext = filename.rsplit(".", 1)[-1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Unsupported file type. Allowed: .csv, .xlsx",
        )


def validate_email_address(raw_email: str) -> str:
    cleaned = raw_email.strip()

    if not cleaned or re.search(r"[\r\n]", cleaned):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
        )

    try:
        email = EmailStr(cleaned)
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
        )

    return str(email)

