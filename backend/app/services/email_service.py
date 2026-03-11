import logging

import httpx

from ..config import settings

logger = logging.getLogger(__name__)


async def send_summary_email(recipient: str, summary: str) -> None:
    if not settings.resend_api_key:
        logger.warning("RESEND_API_KEY not configured; email will not be sent.")
        return

    from_email = settings.resend_from_email or "onboarding@resend.dev"

    payload = {
        "from": from_email,
        "to": [recipient],
        "subject": "Sales Summary Report",
        "text": f"AI Generated Executive Summary\n\n{summary}\n",
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                "https://api.resend.com/emails",
                headers={
                    "Authorization": f"Bearer {settings.resend_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            logger.info("Email successfully sent to %s via Resend", recipient)
    except Exception as exc:
        if isinstance(exc, httpx.HTTPStatusError):
            logger.error("Resend API error %s: %s", exc.response.status_code, exc.response.text)
        logger.exception("Failed to send email to %s: %s", recipient, exc)
        raise
