import logging
from textwrap import dedent

import httpx

from ..config import settings
from ..models.request_models import SalesMetrics

logger = logging.getLogger(__name__)


async def generate_executive_summary(metrics: SalesMetrics) -> str:
    if not settings.groq_api_key:
        logger.warning("GROQ_API_KEY not configured; returning fallback summary")
        return _fallback_summary(metrics)

    prompt = dedent(
        f"""
        Analyze the following sales metrics and generate a concise executive summary suitable for leadership.

        Metrics:
        - Total Revenue: {metrics.total_revenue:,.2f}
        - Top Region: {metrics.top_region or "N/A"}
        - Top Category: {metrics.top_category or "N/A"}
        - Cancelled Orders: {metrics.cancelled_orders}

        Produce a professional summary highlighting performance trends and insights.
        """
    ).strip()

    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            url = "https://api.groq.com/openai/v1/chat/completions"
            headers = {
                "Authorization": f"Bearer {settings.groq_api_key}",
                "Content-Type": "application/json",
            }
            payload = {
                "model": settings.groq_model,
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a senior sales analyst.",
                    },
                    {
                        "role": "user",
                        "content": prompt,
                    },
                ],
                "temperature": 0.3,
            }

            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

            choices = data.get("choices") or []
            if not choices:
                logger.error("Groq API returned no choices: %s", data)
                return _fallback_summary(metrics)

            message = choices[0].get("message") or {}
            summary_text = (message.get("content") or "").strip()
            if not summary_text:
                logger.error("Groq API returned empty summary: %s", data)
                return _fallback_summary(metrics)

            return summary_text
    except Exception as exc:
        logger.exception("Error while calling Groq API: %s", exc)
        return _fallback_summary(metrics)


def _fallback_summary(metrics: SalesMetrics) -> str:
    lines = [
        "Sales Performance Overview:",
        f"- Total revenue recorded: ${metrics.total_revenue:,.2f}.",
        f"- Top performing region: {metrics.top_region or 'not available'}.",
        f"- Leading product category: {metrics.top_category or 'not available'}.",
        f"- Number of cancelled orders: {metrics.cancelled_orders}.",
        "Overall, review regional and category performance to reinforce strengths and investigate drivers behind cancellations.",
    ]
    return "\n".join(lines)

