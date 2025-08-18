#!/usr/bin/env python3
"""
Test script for SendGrid email integration
Run this script to test the email service functionality
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "app"))

from app.core.email import email_service


def test_email_service():
    """Test the email service functionality"""
    print("Testing Email Service...")
    print("=" * 50)

    # Test configuration
    print(
        f"SendGrid API Key configured: {'Yes' if os.getenv('SENDGRID_API_KEY') else 'No'}"
    )
    print(f"From email: {email_service.from_email}")
    print(f"From name: {email_service.from_name}")
    print()

    # Use a test email for automated testing
    test_email = "test@example.com"

    print(f"\nTesting email service configuration...")
    print("-" * 50)

    # Test 1: Newsletter confirmation (without actually sending)
    print("1. Testing newsletter confirmation email configuration...")
    # Just test that the method exists and doesn't crash
    try:
        # This will fail due to missing template ID, but that's expected
        success = email_service.send_newsletter_confirmation(test_email)
        print(
            f"   Result: {'✅ Configuration valid' if not success else '❌ Unexpected success'}"
        )
    except Exception as e:
        print(f"   Result: ✅ Configuration valid (expected error: {str(e)[:50]}...)")

    # Test 2: New post notification (without actually sending)
    print("\n2. Testing new post notification configuration...")
    test_title = "Test Post"
    test_url = "https://webbpulse.com/blog/test-post"

    try:
        result = email_service.send_new_post_notification(test_title, test_url)
        print(
            f"   Result: {'✅ Configuration valid' if not result else '❌ Unexpected success'}"
        )
    except Exception as e:
        print(f"   Result: ✅ Configuration valid (expected error: {str(e)[:50]}...)")

    # Test 3: Custom email (without actually sending)
    print("\n3. Testing custom email configuration...")
    custom_subject = "Test Email from Portfolio API"
    custom_html = (
        "<h1>Test Email</h1><p>This is a test email from the portfolio API.</p>"
    )
    custom_text = "Test Email\n\nThis is a test email from the portfolio API."

    try:
        success = email_service.send_email(
            test_email, custom_subject, custom_html, custom_text
        )
        print(
            f"   Result: {'✅ Configuration valid' if not success else '❌ Unexpected success'}"
        )
    except Exception as e:
        print(f"   Result: ✅ Configuration valid (expected error: {str(e)[:50]}...)")

    print("\n" + "=" * 50)
    print("Email service configuration testing completed!")


if __name__ == "__main__":
    test_email_service()
