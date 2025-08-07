#!/usr/bin/env python3
"""
Comprehensive test script for Portfolio Blog API setup
"""

import os
import sys
from pathlib import Path

def test_config():
    """Test configuration loading"""
    print("🔧 Testing configuration...")
    
    try:
        # Add the current directory to Python path
        sys.path.insert(0, str(Path(__file__).parent))
        
        from app.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   Database URL: {settings.get_database_url()}")
        print(f"   Debug mode: {settings.DEBUG}")
        print(f"   App name: {settings.APP_NAME}")
        return True
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️  Testing database connection...")
    
    try:
        from app.database import test_db_connection
        if test_db_connection():
            print("✅ Database connection successful")
            return True
        else:
            print("❌ Database connection failed")
            return False
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def test_models():
    """Test model imports"""
    print("\n📋 Testing model imports...")
    
    try:
        from app.models import User, Category, Post, Subscriber
        print("✅ All models imported successfully")
        print(f"   Available models: {[User.__name__, Category.__name__, Post.__name__, Subscriber.__name__]}")
        return True
    except Exception as e:
        print(f"❌ Model import error: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    print("\n🚀 Testing FastAPI app...")
    
    try:
        from app.main import app
        print("✅ FastAPI app created successfully")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Portfolio Blog API Setup Test")
    print("=" * 50)
    
    # Test configuration
    config_ok = test_config()
    
    # Test models
    models_ok = test_models()
    
    # Test FastAPI app
    app_ok = test_fastapi_app()
    
    # Test database connection (only if Docker is running)
    db_ok = False
    try:
        import docker
        client = docker.from_env()
        client.ping()
        db_ok = test_database_connection()
    except:
        print("\n🐳 Docker not running - skipping database connection test")
        print("   To test database connection, start Docker and run:")
        print("   docker-compose up -d postgres")
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Configuration: {'✅ PASS' if config_ok else '❌ FAIL'}")
    print(f"   Models: {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"   FastAPI App: {'✅ PASS' if app_ok else '❌ FAIL'}")
    print(f"   Database: {'✅ PASS' if db_ok else '⚠️  SKIP'}")
    
    if config_ok and models_ok and app_ok:
        print("\n🎉 Setup is ready!")
        print("   Next steps:")
        print("   1. Start Docker")
        print("   2. Run: docker-compose up -d postgres")
        print("   3. Run: uvicorn app.main:app --reload")
        print("   4. Access: http://localhost:8000/docs")
    else:
        print("\n❌ Setup has issues. Please check the errors above.")

if __name__ == "__main__":
    main() 