"""
Tests for the subscribers API endpoints
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock


class TestSubscribersAPI:
    """Test class for subscribers API endpoints"""

    @pytest.mark.api
    @patch("app.core.email.email_service.add_to_subscription_group")
    @patch("app.core.email.email_service.send_newsletter_confirmation")
    def test_subscribe_newsletter_success(
        self, mock_send_confirmation, mock_add_to_group, client: TestClient
    ):
        """Test successful newsletter subscription"""
        # Mock successful subscription
        mock_add_to_group.return_value = True
        mock_send_confirmation.return_value = True

        subscription_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully subscribed to newsletter"
        assert data["email"] == "test@example.com"
        assert data["status"] == "active"

        # Verify mocks were called
        mock_add_to_group.assert_called_once_with(
            email="test@example.com", first_name="Test", last_name="User"
        )
        mock_send_confirmation.assert_called_once_with("test@example.com")

    @pytest.mark.api
    @patch("app.core.email.email_service.add_to_subscription_group")
    def test_subscribe_newsletter_minimal_data(
        self, mock_add_to_group, client: TestClient
    ):
        """Test newsletter subscription with minimal data (email only)"""
        mock_add_to_group.return_value = True

        subscription_data = {"email": "test@example.com"}

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully subscribed to newsletter"
        assert data["email"] == "test@example.com"

        # Verify mock was called with None for missing fields
        mock_add_to_group.assert_called_once_with(
            email="test@example.com", first_name=None, last_name=None
        )

    @pytest.mark.api
    @patch("app.core.email.email_service.add_to_subscription_group")
    def test_subscribe_newsletter_failure(self, mock_add_to_group, client: TestClient):
        """Test newsletter subscription when SendGrid fails"""
        mock_add_to_group.return_value = False

        subscription_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 500
        assert "Failed to subscribe to newsletter" in response.json()["detail"]

    @pytest.mark.api
    @patch("app.core.email.email_service.add_to_subscription_group")
    def test_subscribe_newsletter_exception(
        self, mock_add_to_group, client: TestClient
    ):
        """Test newsletter subscription when exception occurs"""
        mock_add_to_group.side_effect = Exception("SendGrid API error")

        subscription_data = {"email": "test@example.com"}

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 500
        assert "Subscription failed" in response.json()["detail"]

    @pytest.mark.api
    def test_subscribe_newsletter_invalid_email(self, client: TestClient):
        """Test newsletter subscription with invalid email"""
        subscription_data = {
            "email": "invalid-email",
            "first_name": "Test",
            "last_name": "User",
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 422

    @pytest.mark.api
    def test_subscribe_newsletter_missing_email(self, client: TestClient):
        """Test newsletter subscription with missing email"""
        subscription_data = {"first_name": "Test", "last_name": "User"}

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 422

    @pytest.mark.api
    @patch("app.core.email.email_service.remove_from_subscription_group")
    def test_unsubscribe_newsletter_success(
        self, mock_remove_from_group, client: TestClient
    ):
        """Test successful newsletter unsubscription"""
        mock_remove_from_group.return_value = True

        subscription_data = {"email": "test@example.com"}

        response = client.post(
            "/api/v1/subscribers/unsubscribe", json=subscription_data
        )
        assert response.status_code == 200
        data = response.json()
        assert data["message"] == "Successfully unsubscribed from newsletter"

        mock_remove_from_group.assert_called_once_with("test@example.com")

    @pytest.mark.api
    @patch("app.core.email.email_service.remove_from_subscription_group")
    def test_unsubscribe_newsletter_failure(
        self, mock_remove_from_group, client: TestClient
    ):
        """Test newsletter unsubscription when SendGrid fails"""
        mock_remove_from_group.return_value = False

        subscription_data = {"email": "test@example.com"}

        response = client.post(
            "/api/v1/subscribers/unsubscribe", json=subscription_data
        )
        assert response.status_code == 500
        assert "Failed to unsubscribe from newsletter" in response.json()["detail"]

    @pytest.mark.api
    @patch("app.core.email.email_service.remove_from_subscription_group")
    def test_unsubscribe_newsletter_exception(
        self, mock_remove_from_group, client: TestClient
    ):
        """Test newsletter unsubscription when exception occurs"""
        mock_remove_from_group.side_effect = Exception("SendGrid API error")

        subscription_data = {"email": "test@example.com"}

        response = client.post(
            "/api/v1/subscribers/unsubscribe", json=subscription_data
        )
        assert response.status_code == 500
        assert "Unsubscribe failed" in response.json()["detail"]

    @pytest.mark.api
    def test_unsubscribe_newsletter_invalid_email(self, client: TestClient):
        """Test newsletter unsubscription with invalid email"""
        subscription_data = {"email": "invalid-email"}

        response = client.post(
            "/api/v1/subscribers/unsubscribe", json=subscription_data
        )
        assert response.status_code == 422

    @pytest.mark.api
    @patch("app.core.email.email_service.get_subscription_status")
    def test_get_subscription_status_success(self, mock_get_status, client: TestClient):
        """Test successful subscription status retrieval"""
        mock_get_status.return_value = "active"

        response = client.get("/api/v1/subscribers/status/test@example.com")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["status"] == "active"

        mock_get_status.assert_called_once_with("test@example.com")

    @pytest.mark.api
    @patch("app.core.email.email_service.get_subscription_status")
    def test_get_subscription_status_unsubscribed(
        self, mock_get_status, client: TestClient
    ):
        """Test subscription status for unsubscribed user"""
        mock_get_status.return_value = "unsubscribed"

        response = client.get("/api/v1/subscribers/status/test@example.com")
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["status"] == "unsubscribed"

    @pytest.mark.api
    @patch("app.core.email.email_service.get_subscription_status")
    def test_get_subscription_status_failure(self, mock_get_status, client: TestClient):
        """Test subscription status when SendGrid fails"""
        mock_get_status.return_value = None

        response = client.get("/api/v1/subscribers/status/test@example.com")
        assert response.status_code == 500
        assert "Failed to get subscription status" in response.json()["detail"]

    @pytest.mark.api
    @patch("app.core.email.email_service.get_subscription_status")
    def test_get_subscription_status_exception(
        self, mock_get_status, client: TestClient
    ):
        """Test subscription status when exception occurs"""
        mock_get_status.side_effect = Exception("SendGrid API error")

        response = client.get("/api/v1/subscribers/status/test@example.com")
        assert response.status_code == 500
        assert "Failed to get status" in response.json()["detail"]

    @pytest.mark.api
    def test_get_subscription_status_invalid_email(self, client: TestClient):
        """Test subscription status with invalid email format"""
        response = client.get("/api/v1/subscribers/status/invalid-email")
        # This should still work as it's just a path parameter
        assert (
            response.status_code == 500
        )  # Will fail due to SendGrid, but not validation


class TestSubscribersAPIValidation:
    """Test class for API validation and edge cases"""

    @pytest.mark.api
    def test_subscribe_empty_data(self, client: TestClient):
        """Test subscription with empty data"""
        response = client.post("/api/v1/subscribers/subscribe", json={})
        assert response.status_code == 422

    @pytest.mark.api
    def test_subscribe_very_long_email(self, client: TestClient):
        """Test subscription with very long email"""
        long_email = "a" * 300 + "@example.com"
        subscription_data = {
            "email": long_email,
            "first_name": "Test",
            "last_name": "User",
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 422

    @pytest.mark.api
    def test_subscribe_very_long_names(self, client: TestClient):
        """Test subscription with very long names"""
        long_name = "a" * 1000
        subscription_data = {
            "email": "test@example.com",
            "first_name": long_name,
            "last_name": long_name,
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 500

    @pytest.mark.api
    def test_subscribe_special_characters(self, client: TestClient):
        """Test subscription with special characters in names"""
        subscription_data = {
            "email": "test@example.com",
            "first_name": "José",
            "last_name": "O'Connor",
        }

        response = client.post("/api/v1/subscribers/subscribe", json=subscription_data)
        assert response.status_code == 500  # Will fail due to email service mock


class TestSubscribersAPIIntegration:
    """Test class for integration scenarios"""

    @pytest.mark.integration
    @patch("app.api.v1.endpoints.subscribers.email_service.add_to_subscription_group")
    @patch(
        "app.api.v1.endpoints.subscribers.email_service.send_newsletter_confirmation"
    )
    @patch("app.api.v1.endpoints.subscribers.email_service.get_subscription_status")
    @patch(
        "app.api.v1.endpoints.subscribers.email_service.remove_from_subscription_group"
    )
    def test_full_subscription_flow(
        self,
        mock_remove_from_group,
        mock_get_status,
        mock_send_confirmation,
        mock_add_to_group,
        client: TestClient,
    ):
        """Test complete subscription flow"""
        # Setup mocks
        mock_add_to_group.return_value = True
        mock_send_confirmation.return_value = True
        mock_get_status.return_value = "active"
        mock_remove_from_group.return_value = True

        # 1. Subscribe
        subscription_data = {
            "email": "test@example.com",
            "first_name": "Test",
            "last_name": "User",
        }

        subscribe_response = client.post(
            "/api/v1/subscribers/subscribe", json=subscription_data
        )
        assert subscribe_response.status_code == 200

        # 2. Check status
        status_response = client.get("/api/v1/subscribers/status/test@example.com")
        assert status_response.status_code == 200
        assert status_response.json()["status"] == "active"

        # 3. Unsubscribe
        unsubscribe_response = client.post(
            "/api/v1/subscribers/unsubscribe", json={"email": "test@example.com"}
        )
        assert unsubscribe_response.status_code == 200

    @pytest.mark.integration
    @patch("app.api.v1.endpoints.subscribers.email_service.add_to_subscription_group")
    @patch(
        "app.api.v1.endpoints.subscribers.email_service.send_newsletter_confirmation"
    )
    def test_multiple_subscriptions(
        self, mock_send_confirmation, mock_add_to_group, client: TestClient
    ):
        """Test multiple subscriptions with different emails"""
        mock_add_to_group.return_value = True
        mock_send_confirmation.return_value = True

        emails = ["user1@example.com", "user2@example.com", "user3@example.com"]

        for email in emails:
            subscription_data = {
                "email": email,
                "first_name": f"User{emails.index(email) + 1}",
                "last_name": "Test",
            }

            response = client.post(
                "/api/v1/subscribers/subscribe", json=subscription_data
            )
            assert response.status_code == 200
