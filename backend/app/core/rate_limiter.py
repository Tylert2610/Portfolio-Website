"""
Rate limiting implementation using sliding window approach.
Suitable for small applications with limited concurrent users.
"""

import logging
import os
import time
from collections import defaultdict
from typing import Dict, List, Optional

from fastapi import Request
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    In-memory rate limiter using sliding window approach.

    This implementation is suitable for small applications with limited
    concurrent users. For production applications with high traffic,
    consider using Redis or a dedicated rate limiting service.
    """

    def __init__(
        self,
        requests_per_minute: int = 60,
        requests_per_hour: int = 1000,
        requests_per_day: int = 10000,
        window_size_seconds: int = 60,
        test_mode: bool = False,
    ):
        """
        Initialize rate limiter with configurable limits.

        Args:
            requests_per_minute: Maximum requests allowed per minute
            requests_per_hour: Maximum requests allowed per hour
            requests_per_day: Maximum requests allowed per day
            window_size_seconds: Size of the sliding window in seconds
            test_mode: If True, rate limiting is disabled (for testing)
        """
        self.requests_per_minute = requests_per_minute
        self.requests_per_hour = requests_per_hour
        self.requests_per_day = requests_per_day
        self.window_size_seconds = window_size_seconds
        self.test_mode = test_mode

        # Store request timestamps for each client
        self.client_requests: Dict[str, List[float]] = defaultdict(list)

        # Store rate limit violations for monitoring
        self.violations: Dict[str, int] = defaultdict(int)

        if test_mode:
            logger.info(
                "Rate limiter initialized in TEST MODE - rate limiting disabled"
            )
        else:
            logger.info(
                f"Rate limiter initialized: {requests_per_minute}/min, "
                f"{requests_per_hour}/hour, {requests_per_day}/day"
            )

    def _get_client_identifier(self, request: Request) -> str:
        """
        Get a unique identifier for the client.

        Args:
            request: FastAPI request object

        Returns:
            Client identifier string
        """
        # Try to get real IP address, considering proxy headers
        client_ip = request.headers.get("X-Forwarded-For")
        if not client_ip:
            client_ip = request.headers.get("X-Real-IP")
        if not client_ip:
            client_ip = request.client.host if request.client else "unknown"

        # Use IP address as identifier
        return client_ip

    def _cleanup_old_requests(self, client_id: str, current_time: float) -> None:
        """
        Remove old requests outside the sliding window.

        Args:
            client_id: Client identifier
            current_time: Current timestamp
        """
        if client_id not in self.client_requests:
            return

        # Remove requests older than the window size
        cutoff_time = current_time - self.window_size_seconds
        self.client_requests[client_id] = [
            req_time
            for req_time in self.client_requests[client_id]
            if req_time > cutoff_time
        ]

    def _check_rate_limit(
        self, client_id: str, current_time: float, limit: int, window_seconds: int
    ) -> bool:
        """
        Check if client has exceeded rate limit for a specific window.

        Args:
            client_id: Client identifier
            current_time: Current timestamp
            limit: Maximum requests allowed
            window_seconds: Window size in seconds

        Returns:
            True if rate limit is exceeded, False otherwise
        """
        if client_id not in self.client_requests:
            return False

        # Get requests within the window
        cutoff_time = current_time - window_seconds
        recent_requests = [
            req_time
            for req_time in self.client_requests[client_id]
            if req_time > cutoff_time
        ]

        return len(recent_requests) >= limit

    def is_rate_limited(self, request: Request) -> tuple[bool, Optional[str]]:
        """
        Check if the request should be rate limited.

        Args:
            request: FastAPI request object

        Returns:
            Tuple of (is_limited, reason)
        """
        # If in test mode, skip rate limiting unless explicitly testing
        if self.test_mode:
            return False, None

        client_id = self._get_client_identifier(request)
        current_time = time.time()

        # Clean up old requests
        self._cleanup_old_requests(client_id, current_time)

        # Check different rate limits
        if self._check_rate_limit(
            client_id, current_time, self.requests_per_minute, 60
        ):
            self.violations[client_id] += 1
            logger.warning(f"Rate limit exceeded for {client_id}: minute limit")
            return True, "Rate limit exceeded: too many requests per minute"

        if self._check_rate_limit(
            client_id, current_time, self.requests_per_hour, 3600
        ):
            self.violations[client_id] += 1
            logger.warning(f"Rate limit exceeded for {client_id}: hour limit")
            return True, "Rate limit exceeded: too many requests per hour"

        if self._check_rate_limit(
            client_id, current_time, self.requests_per_day, 86400
        ):
            self.violations[client_id] += 1
            logger.warning(f"Rate limit exceeded for {client_id}: day limit")
            return True, "Rate limit exceeded: too many requests per day"

        # Add current request to tracking
        self.client_requests[client_id].append(current_time)

        return False, None

    def get_client_stats(self, client_id: str) -> Dict:
        """
        Get statistics for a specific client.

        Args:
            client_id: Client identifier

        Returns:
            Dictionary with client statistics
        """
        current_time = time.time()
        requests = self.client_requests.get(client_id, [])

        # Calculate requests in different time windows
        minute_ago = current_time - 60
        hour_ago = current_time - 3600
        day_ago = current_time - 86400

        return {
            "client_id": client_id,
            "requests_last_minute": len([r for r in requests if r > minute_ago]),
            "requests_last_hour": len([r for r in requests if r > hour_ago]),
            "requests_last_day": len([r for r in requests if r > day_ago]),
            "total_requests": len(requests),
            "violations": self.violations.get(client_id, 0),
            "limits": {
                "per_minute": self.requests_per_minute,
                "per_hour": self.requests_per_hour,
                "per_day": self.requests_per_day,
            },
        }

    def get_global_stats(self) -> Dict:
        """
        Get global rate limiter statistics.

        Returns:
            Dictionary with global statistics
        """
        return {
            "total_clients": len(self.client_requests),
            "total_violations": sum(self.violations.values()),
            "limits": {
                "per_minute": self.requests_per_minute,
                "per_hour": self.requests_per_hour,
                "per_day": self.requests_per_day,
            },
        }

    def reset_client(self, client_id: str) -> None:
        """
        Reset rate limiting for a specific client.

        Args:
            client_id: Client identifier
        """
        if client_id in self.client_requests:
            del self.client_requests[client_id]
        if client_id in self.violations:
            del self.violations[client_id]
        logger.info(f"Rate limiting reset for client: {client_id}")


# Check if we're in test mode
TEST_MODE = os.getenv("TESTING", "false").lower() == "true"

# Global rate limiter instance
rate_limiter = RateLimiter(test_mode=TEST_MODE)


async def rate_limit_middleware(request: Request, call_next):
    """
    FastAPI middleware for rate limiting.

    Args:
        request: FastAPI request object
        call_next: Next middleware/endpoint function

    Returns:
        FastAPI response
    """
    # Skip rate limiting for health check and root endpoints
    if request.url.path in ["/health", "/", "/docs", "/redoc", "/openapi.json"]:
        return await call_next(request)

    # Check rate limit
    is_limited, reason = rate_limiter.is_rate_limited(request)

    if is_limited:
        logger.warning(f"Rate limit exceeded: {request.client.host} - {reason}")
        return JSONResponse(
            status_code=429,
            content={"detail": reason, "error": "Too Many Requests", "retry_after": 60},
            headers={"Retry-After": "60"},
        )

    # Add rate limit headers to response
    response = await call_next(request)

    # Get client stats for headers
    client_id = rate_limiter._get_client_identifier(request)
    stats = rate_limiter.get_client_stats(client_id)

    # Add rate limit headers
    response.headers["X-RateLimit-Limit-Minute"] = str(rate_limiter.requests_per_minute)
    response.headers["X-RateLimit-Limit-Hour"] = str(rate_limiter.requests_per_hour)
    response.headers["X-RateLimit-Limit-Day"] = str(rate_limiter.requests_per_day)
    response.headers["X-RateLimit-Remaining-Minute"] = str(
        max(0, rate_limiter.requests_per_minute - stats["requests_last_minute"])
    )
    response.headers["X-RateLimit-Remaining-Hour"] = str(
        max(0, rate_limiter.requests_per_hour - stats["requests_last_hour"])
    )
    response.headers["X-RateLimit-Remaining-Day"] = str(
        max(0, rate_limiter.requests_per_day - stats["requests_last_day"])
    )

    return response
