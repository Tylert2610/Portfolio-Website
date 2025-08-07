#!/usr/bin/env python3
"""
Script to create the initial admin user for the Portfolio Blog API
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.database import SessionLocal, init_db
from app.models.user import User
from app.core.security import get_password_hash
from app.config import settings


def create_admin_user(username: str, password: str, email: str = None):
    """Create an admin user"""
    db = SessionLocal()

    try:
        # Check if admin user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            print(f"❌ User '{username}' already exists")
            return False

        # Create new admin user
        hashed_password = get_password_hash(password)
        admin_user = User(
            username=username,
            hashed_password=hashed_password,
            email=email,
            is_admin=True,
        )

        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)

        print(f"✅ Admin user '{username}' created successfully")
        print(f"   Username: {username}")
        print(f"   Email: {email or 'Not set'}")
        print(f"   Admin: Yes")
        return True

    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """Main function"""
    print("🔐 Portfolio Blog API - Admin User Creation")
    print("=" * 50)

    # Initialize database if needed
    try:
        init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return

    # Get admin credentials
    print("\n📝 Enter admin user details:")
    username = input("Username: ").strip()
    password = input("Password: ").strip()
    email = input("Email (optional): ").strip() or None

    if not username or not password:
        print("❌ Username and password are required")
        return

    # Create admin user
    print(f"\n🔄 Creating admin user '{username}'...")
    success = create_admin_user(username, password, email)

    if success:
        print("\n🎉 Admin user created successfully!")
        print("You can now log in to the admin panel at:")
        print("  POST /api/v1/admin/login")
        print("\nExample login request:")
        print(f"  {{'username': '{username}', 'password': 'your_password'}}")
    else:
        print("\n❌ Failed to create admin user")


if __name__ == "__main__":
    main()
