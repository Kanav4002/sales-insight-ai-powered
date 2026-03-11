import io
import logging
from typing import Annotated

import pandas as pd
from fastapi import APIRouter, Depends, File, Form, HTTPException, Request, UploadFile, status

from ..models.response_models import UploadResponse
from ..security.rate_limit import rate_limiter
from ..security.validation import validate_email_address, validate_file_upload
from ..services.ai_service import generate_executive_summary
from ..services.email_service import send_summary_email
from ..services.parser import parse_sales_file, calculate_sales_metrics

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/upload",
    response_model=UploadResponse,
    status_code=status.HTTP_200_OK,
    summary="Upload sales data and trigger AI summary generation",
)
async def upload_sales_file(
    request: Request,
    file: Annotated[UploadFile, File(..., description="Sales data file (.csv or .xlsx)")],
    email: Annotated[str, Form(..., description="Recipient email address")],
    _: None = Depends(rate_limiter),
) -> UploadResponse:
    client_ip = request.client.host if request.client else "unknown"
    logger.info("Upload received from IP=%s, filename=%s", client_ip, file.filename)

    validate_file_upload(file)
    recipient_email = validate_email_address(email)

    content_length = request.headers.get("content-length")
    max_bytes = 5 * 1024 * 1024
    if content_length is not None:
        try:
            if int(content_length) > max_bytes:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail="File size exceeds 5MB limit",
                )
        except ValueError:
            pass

    try:
        raw_bytes = await file.read()
        if len(raw_bytes) > max_bytes:
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="File size exceeds 5MB limit",
            )

        buffer = io.BytesIO(raw_bytes)
        df: pd.DataFrame = parse_sales_file(buffer, file.filename)

        logger.info("File parsed successfully for IP=%s, records=%d", client_ip, len(df))

        metrics = calculate_sales_metrics(df)
        logger.info("Sales metrics calculated for IP=%s", client_ip)

        summary = await generate_executive_summary(metrics)
        logger.info("AI summary generated for IP=%s", client_ip)

        await send_summary_email(recipient_email, summary)
        logger.info("Summary email sent to %s for IP=%s", recipient_email, client_ip)

        return UploadResponse(
            status="success",
            message="Summary generated and emailed",
        )
    except HTTPException:
        raise
    except Exception as exc:
        logger.exception("Error processing upload from IP=%s: %s", client_ip, exc)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while processing file",
        ) from exc

