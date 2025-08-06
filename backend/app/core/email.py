import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
import boto3
from botocore.exceptions import ClientError
from ..config import settings


class EmailService:
    def __init__(self):
        self.from_email = settings.EMAIL_FROM
        
        # Initialize AWS SES if credentials are provided
        if settings.AWS_ACCESS_KEY_ID and settings.AWS_SECRET_ACCESS_KEY:
            self.ses_client = boto3.client(
                'ses',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_REGION
            )
            self.use_ses = True
        else:
            self.use_ses = False
    
    def send_email_ses(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using AWS SES"""
        try:
            response = self.ses_client.send_email(
                Source=self.from_email,
                Destination={'ToAddresses': [to_email]},
                Message={
                    'Subject': {'Data': subject},
                    'Body': {
                        'Text': {'Data': text_content},
                        'Html': {'Data': html_content}
                    }
                }
            )
            return True
        except ClientError as e:
            print(f"Error sending email via SES: {e}")
            return False
    
    def send_email_smtp(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SMTP"""
        if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
            print("SMTP settings not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = self.from_email
            msg['To'] = to_email
            
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Error sending email via SMTP: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using the configured method"""
        if self.use_ses:
            return self.send_email_ses(to_email, subject, html_content, text_content)
        else:
            return self.send_email_smtp(to_email, subject, html_content, text_content)
    
    def send_newsletter_confirmation(self, email: str) -> bool:
        """Send newsletter subscription confirmation email"""
        subject = "Welcome to the Newsletter!"
        html_content = f"""
        <html>
            <body>
                <h2>Welcome to the Newsletter!</h2>
                <p>Thank you for subscribing to our newsletter. You'll now receive updates about new blog posts and tech insights.</p>
                <p>Best regards,<br>Tyler Webb</p>
            </body>
        </html>
        """
        text_content = f"""
        Welcome to the Newsletter!
        
        Thank you for subscribing to our newsletter. You'll now receive updates about new blog posts and tech insights.
        
        Best regards,
        Tyler Webb
        """
        
        return self.send_email(email, subject, html_content, text_content)
    
    def send_new_post_notification(self, subscribers: List[str], post_title: str, post_url: str) -> bool:
        """Send new post notification to all subscribers"""
        subject = f"New Blog Post: {post_title}"
        html_content = f"""
        <html>
            <body>
                <h2>New Blog Post Available!</h2>
                <p>A new blog post has been published: <strong>{post_title}</strong></p>
                <p><a href="{post_url}">Read the full post here</a></p>
                <p>Best regards,<br>Tyler Webb</p>
            </body>
        </html>
        """
        text_content = f"""
        New Blog Post Available!
        
        A new blog post has been published: {post_title}
        
        Read the full post here: {post_url}
        
        Best regards,
        Tyler Webb
        """
        
        success_count = 0
        for subscriber_email in subscribers:
            if self.send_email(subscriber_email, subject, html_content, text_content):
                success_count += 1
        
        return success_count > 0


# Create global email service instance
email_service = EmailService() 