import certifi
import logging
import smtplib
import ssl
from email.message import EmailMessage

from ..config import settings

logger = logging.getLogger(__name__)


async def send_summary_email(recipient: str, summary: str) -> None:
    if not settings.smtp_host or not settings.smtp_user or not settings.smtp_password:
        logger.warning(
            "SMTP configuration incomplete; email will not be sent."
        )
        return

    from_email = settings.smtp_from_email or settings.smtp_user

    message = EmailMessage()
    message["Subject"] = "Sales Summary Report"
    message["From"] = from_email
    message["To"] = recipient
    body = (
        "AI Generated Executive Summary\n\n"
        f"{summary}\n"
    )
    message.set_content(body)

    context = ssl.create_default_context(cafile=certifi.where())
    try:
        with smtplib.SMTP(settings.smtp_host, settings.smtp_port, timeout=15) as server:
            server.starttls(context=context)
            server.login(settings.smtp_user, settings.smtp_password)
            server.send_message(message)
            logger.info("Email successfully sent to %s", recipient)
    except Exception as exc:
        logger.exception("Failed to send email to %s: %s", recipient, exc)
        raise
