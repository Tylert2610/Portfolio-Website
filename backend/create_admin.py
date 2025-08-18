#!/usr/bin/env python3
"""
Script to create the initial admin user for the Portfolio Blog API
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings
from app.core.security import get_password_hash
from app.database import SessionLocal as DefaultSessionLocal
from app.database import init_db
from app.models.user import User


def create_admin_user(username: str, password: str, email: str = None, SessionLocal=None):
    """Create an admin user"""
    if SessionLocal is None:
        SessionLocal = DefaultSessionLocal
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
    import argparse

    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    parser = argparse.ArgumentParser(description="Create an admin user.")
    parser.add_argument("--username", help="Admin username")
    parser.add_argument("--password", help="Admin password")
    parser.add_argument("--email", help="Admin email")
    parser.add_argument("--db-url", help="Override the database URL")
    args = parser.parse_args()

    # If username/password not provided as flags, prompt interactively
    username = args.username or input("Username: ").strip()
    password = args.password or input("Password: ").strip()
    email = args.email or (input("Email (optional): ").strip() or None)

    if not username or not password:
        print("❌ Username and password are required")
        return

    # Optionally override SessionLocal
    SessionLocal = None
    if args.db_url:
        engine = create_engine(args.db_url, pool_pre_ping=True)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    print(f"\n🔄 Creating admin user '{username}'...")
    success = create_admin_user(username, password, email, SessionLocal=SessionLocal)

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
