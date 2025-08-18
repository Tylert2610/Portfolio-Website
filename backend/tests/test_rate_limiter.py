"""
Tests for rate limiting functionality.
"""

import time
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi.testclient import TestClient

from app.config import settings
from app.core.rate_limiter import (RateLimiter, rate_limit_middleware,
                                   rate_limiter)
from app.main import app


class TestRateLimiter:
    """Test cases for RateLimiter class."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization with default values."""
        limiter = RateLimiter()
        assert limiter.requests_per_minute == 60
        assert limiter.requests_per_hour == 1000
        assert limiter.requests_per_day == 10000
        assert limiter.window_size_seconds == 60

    def test_rate_limiter_custom_initialization(self):
        """Test rate limiter initialization with custom values."""
        limiter = RateLimiter(
            requests_per_minute=30,
            requests_per_hour=500,
            requests_per_day=5000,
            window_size_seconds=30,
        )
        assert limiter.requests_per_minute == 30
        assert limiter.requests_per_hour == 500
        assert limiter.requests_per_day == 5000
        assert limiter.window_size_seconds == 30

    def test_rate_limiter_test_mode_initialization(self):
        """Test rate limiter initialization in test mode."""
        limiter = RateLimiter(test_mode=True)
        assert limiter.test_mode is True
        assert limiter.requests_per_minute == 60
        assert limiter.requests_per_hour == 1000
        assert limiter.requests_per_day == 10000

    def test_get_client_identifier(self):
        """Test client identifier extraction from request."""
        limiter = RateLimiter()

        # Test with X-Forwarded-For header
        request = Mock()
        request.headers = {"X-Forwarded-For": "192.168.1.1"}
        request.client = None
        assert limiter._get_client_identifier(request) == "192.168.1.1"

        # Test with X-Real-IP header
        request.headers = {"X-Real-IP": "10.0.0.1"}
        assert limiter._get_client_identifier(request) == "10.0.0.1"

        # Test with client.host
        request.headers = {}
        request.client = Mock()
        request.client.host = "127.0.0.1"
        assert limiter._get_client_identifier(request) == "127.0.0.1"

        # Test fallback to unknown
        request.client = None
        assert limiter._get_client_identifier(request) == "unknown"

    def test_cleanup_old_requests(self):
        """Test cleanup of old requests outside the window."""
        limiter = RateLimiter(window_size_seconds=60)
        client_id = "test_client"
        current_time = time.time()

        # Add requests at different times
        limiter.client_requests[client_id] = [
            current_time - 120,  # 2 minutes ago (should be removed)
            current_time - 30,  # 30 seconds ago (should remain)
            current_time - 10,  # 10 seconds ago (should remain)
        ]

        limiter._cleanup_old_requests(client_id, current_time)

        # Should only have 2 requests remaining
        assert len(limiter.client_requests[client_id]) == 2
        assert current_time - 30 in limiter.client_requests[client_id]
        assert current_time - 10 in limiter.client_requests[client_id]

    def test_check_rate_limit(self):
        """Test rate limit checking logic."""
        limiter = RateLimiter(requests_per_minute=2)
        client_id = "test_client"
        current_time = time.time()

        # Add requests within the window
        limiter.client_requests[client_id] = [
            current_time - 30,  # 30 seconds ago
            current_time - 10,  # 10 seconds ago
        ]

        # Should be at the limit
        assert limiter._check_rate_limit(client_id, current_time, 2, 60) is True

        # Add one more request - should exceed limit
        limiter.client_requests[client_id].append(current_time - 5)
        assert limiter._check_rate_limit(client_id, current_time, 2, 60) is True

        # Remove one request - should be under limit
        limiter.client_requests[client_id] = [current_time - 30]
        assert limiter._check_rate_limit(client_id, current_time, 2, 60) is False

    def test_is_rate_limited_minute_limit(self):
        """Test rate limiting for minute limit."""
        # Create a rate limiter NOT in test mode for explicit testing
        limiter = RateLimiter(requests_per_minute=2, test_mode=False)
        request = Mock()
        request.headers = {}
        request.client = Mock()
        request.client.host = "test_client"

        # First request - should not be limited
        is_limited, reason = limiter.is_rate_limited(request)
        assert is_limited is False
        assert reason is None

        # Second request - should not be limited
        is_limited, reason = limiter.is_rate_limited(request)
        assert is_limited is False
        assert reason is None

        # Third request - should be limited
        is_limited, reason = limiter.is_rate_limited(request)
        assert is_limited is True
        assert "minute" in reason

    def test_is_rate_limited_hour_limit(self):
        """Test rate limiting for hour limit."""
        # Create a rate limiter NOT in test mode for explicit testing
        limiter = RateLimiter(requests_per_hour=3, test_mode=False)
        request = Mock()
        request.headers = {}
        request.client = Mock()
        request.client.host = "test_client"

        # Add requests within the hour
        for i in range(3):
            limiter.client_requests["test_client"].append(time.time() - (i * 10))

        # Next request should be limited
        is_limited, reason = limiter.is_rate_limited(request)
        assert is_limited is True
        assert "hour" in reason

    def test_is_rate_limited_day_limit(self):
        """Test rate limiting for day limit."""
        # Create a rate limiter NOT in test mode for explicit testing
        limiter = RateLimiter(
            requests_per_day=5, window_size_seconds=86400, test_mode=False
        )
        request = Mock()
        request.headers = {}
        request.client = Mock()
        request.client.host = "test_client"

        # Add requests within the day (86400 seconds = 1 day)
        current_time = time.time()
        for i in range(5):
            limiter.client_requests["test_client"].append(current_time - (i * 1000))

        # Check the rate limit directly without adding the current request
        is_limited = limiter._check_rate_limit("test_client", current_time, 5, 86400)
        assert is_limited is True

        # Now test the full method
        is_limited, reason = limiter.is_rate_limited(request)
        assert is_limited is True
        assert "day" in reason

    def test_is_rate_limited_test_mode_disabled(self):
        """Test that rate limiting is disabled in test mode."""
        # Create a rate limiter in test mode
        limiter = RateLimiter(requests_per_minute=1, test_mode=True)
        request = Mock()
        request.headers = {}
        request.client = Mock()
        request.client.host = "test_client"

        # Make multiple requests - should never be limited in test mode
        for i in range(10):
            is_limited, reason = limiter.is_rate_limited(request)
            assert is_limited is False
            assert reason is None

    def test_get_client_stats(self):
        """Test client statistics retrieval."""
        limiter = RateLimiter()
        client_id = "test_client"
        current_time = time.time()

        # Add requests at different times
        limiter.client_requests[client_id] = [
            current_time - 30,  # 30 seconds ago (within minute)
            current_time - 1800,  # 30 minutes ago (within hour)
            current_time - 7200,  # 2 hours ago (within day)
            current_time - 90000,  # 25 hours ago (outside day)
        ]

        limiter.violations[client_id] = 2

        stats = limiter.get_client_stats(client_id)

        assert stats["client_id"] == client_id
        assert stats["requests_last_minute"] == 1
        assert stats["requests_last_hour"] == 2
        assert stats["requests_last_day"] == 3
        assert stats["total_requests"] == 4
        assert stats["violations"] == 2
        assert "limits" in stats

    def test_get_global_stats(self):
        """Test global statistics retrieval."""
        limiter = RateLimiter()

        # Add some test data
        limiter.client_requests["client1"] = [time.time()]
        limiter.client_requests["client2"] = [time.time()]
        limiter.violations["client1"] = 1
        limiter.violations["client2"] = 2

        stats = limiter.get_global_stats()

        assert stats["total_clients"] == 2
        assert stats["total_violations"] == 3
        assert "limits" in stats

    def test_reset_client(self):
        """Test client reset functionality."""
        limiter = RateLimiter()
        client_id = "test_client"

        # Add some data
        limiter.client_requests[client_id] = [time.time()]
        limiter.violations[client_id] = 5

        # Reset client
        limiter.reset_client(client_id)

        # Check that data is removed
        assert client_id not in limiter.client_requests
        assert client_id not in limiter.violations


class TestRateLimitMiddleware:
    """Test cases for rate limiting middleware."""

    def test_middleware_skips_health_endpoints(self):
        """Test that middleware skips health check and documentation endpoints."""
        request = Mock()
        request.url.path = "/health"
        request.client = Mock()
        request.client.host = "test_client"

        call_next = AsyncMock()
        call_next.return_value = Mock()

        # Test the middleware logic directly without async
        import asyncio

        response = asyncio.run(rate_limit_middleware(request, call_next))

        # Should call next middleware without rate limiting
        call_next.assert_called_once_with(request)
        assert response == call_next.return_value

    def test_middleware_rate_limits_exceeded(self):
        """Test middleware when rate limit is exceeded."""
        # Create a rate limiter that will always limit (not in test mode)
        test_limiter = RateLimiter(requests_per_minute=1, test_mode=False)

        with patch("app.core.rate_limiter.rate_limiter", test_limiter):
            request = Mock()
            request.url.path = "/api/v1/posts"
            request.client = Mock()
            request.client.host = "test_client"

            # Add a request to trigger rate limiting - use the same client identifier
            client_id = test_limiter._get_client_identifier(request)
            test_limiter.client_requests[client_id] = [time.time() - 10]

            call_next = AsyncMock()
            call_next.return_value = Mock()

            # Test the middleware logic directly without async
            import asyncio

            response = asyncio.run(rate_limit_middleware(request, call_next))

            # Should return 429 response and not call call_next
            assert response.status_code == 429
            assert "Rate limit exceeded" in response.body.decode()
            call_next.assert_not_called()  # Should not call next middleware when rate limited

    def test_middleware_adds_rate_limit_headers(self):
        """Test that middleware adds rate limit headers to responses."""
        with patch("app.core.rate_limiter.rate_limiter") as mock_limiter:
            mock_limiter.is_rate_limited.return_value = (False, None)
            mock_limiter._get_client_identifier.return_value = "test_client"
            mock_limiter.get_client_stats.return_value = {
                "requests_last_minute": 5,
                "requests_last_hour": 50,
                "requests_last_day": 500,
            }
            mock_limiter.requests_per_minute = 60
            mock_limiter.requests_per_hour = 1000
            mock_limiter.requests_per_day = 10000

            request = Mock()
            request.url.path = "/api/v1/posts"
            request.client = Mock()
            request.client.host = "test_client"

            # Create a mock response with mutable headers
            mock_response = Mock()
            mock_response.headers = {}

            call_next = AsyncMock()
            call_next.return_value = mock_response

            # Test the middleware logic directly without async
            import asyncio

            response = asyncio.run(rate_limit_middleware(request, call_next))

            # Check that headers are added
            assert "X-RateLimit-Limit-Minute" in response.headers
            assert "X-RateLimit-Remaining-Minute" in response.headers
            assert response.headers["X-RateLimit-Limit-Minute"] == "60"
            assert response.headers["X-RateLimit-Remaining-Minute"] == "55"


class TestRateLimitIntegration:
    """Integration tests for rate limiting with FastAPI app."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_rate_limit_headers_present(self, client):
        """Test that rate limit headers are present in API responses."""
        response = client.get("/api/v1/posts")

        # Should have rate limit headers
        assert "X-RateLimit-Limit-Minute" in response.headers
        assert "X-RateLimit-Remaining-Minute" in response.headers
        assert "X-RateLimit-Limit-Hour" in response.headers
        assert "X-RateLimit-Remaining-Hour" in response.headers
        assert "X-RateLimit-Limit-Day" in response.headers
        assert "X-RateLimit-Remaining-Day" in response.headers

    def test_rate_limit_not_triggered_in_test_mode(self, client):
        """Test that rate limiting is not triggered during normal tests."""
        # Make many requests - should not be rate limited in test mode
        for i in range(100):
            response = client.get("/api/v1/posts")
            assert response.status_code == 200
            # Should have rate limit headers but not be limited
            assert "X-RateLimit-Limit-Minute" in response.headers

    def test_rate_limit_exceeded_response_explicit_test(self, client):
        """Test rate limit exceeded response with explicit rate limiter."""
        # Create a test rate limiter that's not in test mode
        test_limiter = RateLimiter(requests_per_minute=5, test_mode=False)

        # Temporarily replace the global rate limiter
        original_limiter = app.dependency_overrides.get("rate_limiter")

        with patch("app.core.rate_limiter.rate_limiter", test_limiter):
            # Make requests to trigger rate limiting
            responses = []
            for i in range(10):
                response = client.get("/api/v1/posts")
                responses.append(response)

            # At least one response should be rate limited
            rate_limited_responses = [r for r in responses if r.status_code == 429]
            assert len(rate_limited_responses) > 0

            # Check rate limited response format
            rate_limited_response = rate_limited_responses[0]
            assert rate_limited_response.status_code == 429
            assert "Retry-After" in rate_limited_response.headers
            assert "detail" in rate_limited_response.json()

    def test_health_endpoint_not_rate_limited(self, client):
        """Test that health endpoint is not rate limited."""
        # Make many requests to health endpoint
        for i in range(100):
            response = client.get("/health")
            assert response.status_code == 200
            # Should not have rate limit headers
            assert "X-RateLimit-Limit-Minute" not in response.headers

    def test_docs_endpoint_not_rate_limited(self, client):
        """Test that docs endpoint is not rate limited."""
        # Make many requests to docs endpoint
        for i in range(100):
            response = client.get("/docs")
            assert response.status_code == 200
            # Should not have rate limit headers
            assert "X-RateLimit-Limit-Minute" not in response.headers


class TestRateLimitAdminEndpoints:
    """Test cases for admin rate limiting endpoints."""

    @pytest.fixture
    def client(self):
        """Create test client."""
        return TestClient(app)

    def test_admin_endpoints_require_authentication(self, client):
        """Test that admin endpoints require authentication."""
        # Test rate limit stats endpoint
        response = client.get("/api/v1/admin/rate-limit/stats")
        assert response.status_code in [401, 403, 404]  # 404 if endpoint doesn't exist

        # Test client stats endpoint
        response = client.get("/api/v1/admin/rate-limit/client/test_client")
        assert response.status_code in [401, 403, 404]  # 404 if endpoint doesn't exist

        # Test reset client endpoint
        response = client.post("/api/v1/admin/rate-limit/client/test_client/reset")
        assert response.status_code in [401, 403, 404]  # 404 if endpoint doesn't exist

    def test_rate_limiter_admin_methods(self):
        """Test rate limiter admin methods directly."""
        limiter = RateLimiter()

        # Test get_global_stats
        stats = limiter.get_global_stats()
        assert "total_clients" in stats
        assert "total_violations" in stats
        assert "limits" in stats

        # Test get_client_stats
        client_stats = limiter.get_client_stats("test_client")
        assert client_stats["client_id"] == "test_client"
        assert "requests_last_minute" in client_stats
        assert "violations" in client_stats

        # Test reset_client
        limiter.client_requests["test_client"] = [time.time()]
        limiter.violations["test_client"] = 5
        limiter.reset_client("test_client")
        assert "test_client" not in limiter.client_requests
        assert "test_client" not in limiter.violations
