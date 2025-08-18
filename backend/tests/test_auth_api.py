"""
Tests for the authentication API endpoints
"""

from datetime import datetime, timedelta

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


class TestAuthAPI:
    """Test class for authentication API endpoints"""

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_success(self, client: TestClient, test_admin_user):
        """Test successful admin login"""
        login_data = {"username": "adminuser", "password": "adminpassword123"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert isinstance(data["access_token"], str)
        assert len(data["access_token"]) > 0

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_invalid_username(self, client: TestClient):
        """Test login with invalid username"""
        login_data = {"username": "nonexistentuser", "password": "password123"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_invalid_password(self, client: TestClient, test_admin_user):
        """Test login with invalid password"""
        login_data = {"username": "adminuser", "password": "wrongpassword"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 401
        assert "Incorrect username or password" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_non_admin_user(self, client: TestClient, test_user):
        """Test login with non-admin user (should still work)"""
        login_data = {"username": "testuser", "password": "testpassword123"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_inactive_user(self, client: TestClient, db_session: Session):
        """Test login with inactive user"""
        from app.core.security import get_password_hash
        from app.models import User

        inactive_user = User(
            email="inactive@example.com",
            username="inactiveuser",
            hashed_password=get_password_hash("password123"),
            is_admin=False,
            is_active=False,
        )
        db_session.add(inactive_user)
        db_session.commit()

        login_data = {"username": "inactiveuser", "password": "password123"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 200  # Login should still work
        data = response.json()
        assert "access_token" in data

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_missing_fields(self, client: TestClient):
        """Test login with missing fields"""
        # Missing username
        login_data = {"password": "password123"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 422

        # Missing password
        login_data = {"username": "adminuser"}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 422

        # Empty data
        response = client.post("/api/v1/admin/login", json={})
        assert response.status_code == 422

    @pytest.mark.api
    @pytest.mark.auth
    def test_login_empty_strings(self, client: TestClient):
        """Test login with empty strings"""
        login_data = {"username": "", "password": ""}
        response = client.post("/api/v1/admin/login", json=login_data)
        assert response.status_code == 422


class TestTokenValidation:
    """Test class for token validation and authorization"""

    @pytest.mark.api
    @pytest.mark.auth
    def test_valid_token_access(self, client: TestClient, admin_auth_headers):
        """Test accessing protected endpoint with valid token"""
        # Use the admin auth headers to access a protected endpoint
        response = client.get("/api/v1/posts/admin", headers=admin_auth_headers)
        assert response.status_code == 200

    @pytest.mark.api
    @pytest.mark.auth
    def test_invalid_token_access(self, client: TestClient, invalid_auth_headers):
        """Test accessing protected endpoint with invalid token"""
        response = client.get("/api/v1/posts/admin", headers=invalid_auth_headers)
        assert response.status_code == 401
        assert "Invalid authentication credentials" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.auth
    def test_missing_token_access(self, client: TestClient):
        """Test accessing protected endpoint without token"""
        response = client.get("/api/v1/posts/admin")
        assert response.status_code == 403

    @pytest.mark.api
    @pytest.mark.auth
    def test_non_admin_token_access(self, client: TestClient, auth_headers):
        """Test accessing admin endpoint with non-admin token"""
        response = client.get("/api/v1/posts/admin", headers=auth_headers)
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]

    @pytest.mark.api
    @pytest.mark.auth
    def test_token_with_nonexistent_user(self, client: TestClient, db_session: Session):
        """Test token with user that no longer exists"""
        from app.core.security import create_access_token

        # Create token for non-existent user
        token = create_access_token(data={"sub": "nonexistentuser"})
        headers = {"Authorization": f"Bearer {token}"}

        response = client.get("/api/v1/posts/admin", headers=headers)
        assert response.status_code == 403
        assert "Not enough permissions" in response.json()["detail"]


class TestPasswordSecurity:
    """Test class for password security features"""

    @pytest.mark.unit
    def test_password_hashing(self, test_user):
        """Test that passwords are properly hashed"""
        from app.core.security import verify_password

        # Password should be hashed
        assert test_user.hashed_password != "testpassword123"
        assert test_user.hashed_password.startswith("$2b$")

        # Should verify correctly
        assert verify_password("testpassword123", test_user.hashed_password)
        assert not verify_password("wrongpassword", test_user.hashed_password)

    @pytest.mark.unit
    def test_password_hash_uniqueness(self, db_session: Session):
        """Test that password hashes are unique for same password"""
        from app.core.security import get_password_hash
        from app.models import User

        # Create two users with same password
        user1 = User(
            email="user1@example.com",
            username="user1",
            hashed_password=get_password_hash("samepassword"),
            is_admin=False,
            is_active=True,
        )

        user2 = User(
            email="user2@example.com",
            username="user2",
            hashed_password=get_password_hash("samepassword"),
            is_admin=False,
            is_active=True,
        )

        # Hashes should be different (due to salt)
        assert user1.hashed_password != user2.hashed_password


class TestAuthIntegration:
    """Test class for authentication integration scenarios"""

    @pytest.mark.integration
    @pytest.mark.auth
    def test_full_auth_flow(self, client: TestClient, test_admin_user):
        """Test complete authentication flow"""
        # 1. Login
        login_data = {"username": "adminuser", "password": "adminpassword123"}
        login_response = client.post("/api/v1/admin/login", json=login_data)
        assert login_response.status_code == 200
        token_data = login_response.json()

        # 2. Use token to access protected endpoint
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}
        protected_response = client.get("/api/v1/posts/admin", headers=headers)
        assert protected_response.status_code == 200

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_with_multiple_requests(self, client: TestClient, test_admin_user):
        """Test authentication across multiple requests"""
        # Login
        login_data = {"username": "adminuser", "password": "adminpassword123"}
        login_response = client.post("/api/v1/admin/login", json=login_data)
        token_data = login_response.json()
        headers = {"Authorization": f"Bearer {token_data['access_token']}"}

        # Make multiple requests with same token
        endpoints = ["/api/v1/posts/admin", "/api/v1/projects/", "/api/v1/experience/"]

        for endpoint in endpoints:
            response = client.get(endpoint, headers=headers)
            # Some endpoints require admin, some don't
            assert response.status_code in [200, 403]

    @pytest.mark.integration
    @pytest.mark.auth
    def test_auth_error_handling(self, client: TestClient):
        """Test various authentication error scenarios"""
        # Test malformed token
        headers = {"Authorization": "Bearer malformed.token.here"}
        response = client.get("/api/v1/posts/admin", headers=headers)
        assert response.status_code == 401

        # Test expired token (if we had a way to create one)
        # This would require mocking the token creation with a past expiration

        # Test token with wrong format
        headers = {"Authorization": "Bearer not-a-jwt-token"}
        response = client.get("/api/v1/posts/admin", headers=headers)
        assert response.status_code == 401
