#!/usr/bin/env python3
"""
Test script to verify Railway configuration works correctly
"""

import os
import sys
from pathlib import Path


def test_railway_config():
    """Test Railway DATABASE_URL configuration"""
    print("🔧 Testing Railway configuration...")

    try:
        # Add the current directory to Python path
        sys.path.insert(0, str(Path(__file__).parent))

        from app.config import settings

        # Test with DATABASE_URL (Railway scenario)
        print("✅ Configuration loaded successfully")

        # Test database URL resolution
        try:
            db_url = settings.get_database_url()
            print(
                f"✅ Database URL resolved: {db_url[:20]}..."
                if len(db_url) > 20
                else f"✅ Database URL: {db_url}"
            )
        except ValueError as e:
            print(f"⚠️  Database URL error (expected for local dev): {e}")

        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False


def test_railway_env_vars():
    """Test Railway environment variable handling"""
    print("\n🔧 Testing Railway environment variables...")

    # Simulate Railway environment
    test_db_url = "postgresql://user:pass@host:5432/db"

    # Store original environment
    original_env = {}
    for key in [
        "DATABASE_URL",
        "POSTGRES_DB",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_HOST",
    ]:
        if key in os.environ:
            original_env[key] = os.environ[key]
            del os.environ[key]

    try:
        # Set Railway DATABASE_URL
        os.environ["DATABASE_URL"] = test_db_url

        # Reimport settings to pick up new environment
        import importlib
        import app.config

        importlib.reload(app.config)

        from app.config import settings

        db_url = settings.get_database_url()

        if db_url == test_db_url:
            print("✅ Railway DATABASE_URL handling works correctly")
            return True
        else:
            print(f"❌ Expected {test_db_url}, got {db_url}")
            return False
    except Exception as e:
        print(f"❌ Railway config test failed: {e}")
        return False
    finally:
        # Clean up - restore original environment
        for key in [
            "DATABASE_URL",
            "POSTGRES_DB",
            "POSTGRES_USER",
            "POSTGRES_PASSWORD",
            "POSTGRES_HOST",
        ]:
            if key in os.environ:
                del os.environ[key]
            if key in original_env:
                os.environ[key] = original_env[key]


if __name__ == "__main__":
    print("🚀 Testing Railway Configuration")
    print("=" * 40)

    success = True
    success &= test_railway_config()
    success &= test_railway_env_vars()

    print("\n" + "=" * 40)
    if success:
        print("🎉 All Railway configuration tests passed!")
    else:
        print("❌ Some tests failed. Please check the configuration.")

    sys.exit(0 if success else 1)
