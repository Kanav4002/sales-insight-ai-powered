import logging
import time
from collections import defaultdict, deque
from typing import Deque, Dict

from fastapi import Depends, HTTPException, Request, status

from ..config import settings

logger = logging.getLogger(__name__)


_requests_per_ip: Dict[str, Deque[float]] = defaultdict(deque)


def get_client_ip(request: Request) -> str:
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    if request.client:
        return request.client.host
    return "unknown"


def rate_limiter(request: Request = Depends()) -> None:
    ip = get_client_ip(request)
    now = time.time()
    window_seconds = 60
    max_requests = settings.rate_limit_requests_per_minute

    dq = _requests_per_ip[ip]

    # Drop timestamps older than window
    while dq and dq[0] <= now - window_seconds:
        dq.popleft()

    if len(dq) >= max_requests:
        logger.warning("Rate limit exceeded for IP=%s", ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )

    dq.append(now)

