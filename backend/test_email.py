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
sys.path.append(os.path.join(os.path.dirname(__file__), 'app'))

from app.core.email import email_service

def test_email_service():
    """Test the email service functionality"""
    print("Testing Email Service...")
    print("=" * 50)
    
    # Test configuration
    print(f"SendGrid API Key configured: {'Yes' if os.getenv('SENDGRID_API_KEY') else 'No'}")
    print(f"SMTP configured: {'Yes' if os.getenv('SMTP_HOST') else 'No'}")
    print(f"From email: {email_service.from_email}")
    print(f"From name: {email_service.from_name}")
    print()
    
    # Test email addresses (replace with your test email)
    test_email = input("Enter your email address for testing: ").strip()
    
    if not test_email:
        print("No email address provided. Exiting.")
        return
    
    print(f"\nSending test emails to: {test_email}")
    print("-" * 50)
    
    # Test 1: Newsletter confirmation
    print("1. Testing newsletter confirmation email...")
    success = email_service.send_newsletter_confirmation(test_email)
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    # Test 2: New post notification
    print("\n2. Testing new post notification email...")
    success = email_service.send_new_post_notification(
        [test_email], 
        "Test Blog Post", 
        "https://portfolio.webbpulse.com/blog/test-post"
    )
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    # Test 3: Custom email
    print("\n3. Testing custom email...")
    success = email_service.send_email(
        test_email,
        "SendGrid Integration Test",
        "<h1>Test Email</h1><p>This is a test email to verify SendGrid integration.</p>",
        "Test Email\n\nThis is a test email to verify SendGrid integration."
    )
    print(f"   Result: {'✅ Success' if success else '❌ Failed'}")
    
    print("\n" + "=" * 50)
    print("Email testing complete!")
    print("Check your email inbox for the test messages.")

if __name__ == "__main__":
    test_email_service() 