import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Optional
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content, HtmlContent, PlainTextContent
from ..config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.from_name = settings.SENDGRID_FROM_NAME
        
        # Initialize SendGrid if API key is provided
        if settings.SENDGRID_API_KEY:
            self.sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            self.use_sendgrid = True
            logger.info("SendGrid email service initialized")
        else:
            self.use_sendgrid = False
            logger.warning("SendGrid API key not provided, falling back to SMTP")
    
    def send_email_sendgrid(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SendGrid API"""
        try:
            from_email = Email(self.from_email, self.from_name)
            to_email_obj = To(to_email)
            
            # Create email content
            html_content_obj = HtmlContent(html_content)
            text_content_obj = PlainTextContent(text_content)
            
            # Create mail object
            mail = Mail(from_email, to_email_obj, subject, text_content_obj)
            mail.add_content(html_content_obj)
            
            # Send email
            response = self.sendgrid_client.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Email sent successfully to {to_email} via SendGrid")
                return True
            else:
                logger.error(f"SendGrid API error: {response.status_code} - {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending email via SendGrid: {e}")
            return False
    
    def send_email_smtp(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SMTP (fallback method)"""
        if not all([settings.SMTP_HOST, settings.SMTP_USER, settings.SMTP_PASSWORD]):
            logger.error("SMTP settings not configured")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            text_part = MIMEText(text_content, 'plain')
            html_part = MIMEText(html_content, 'html')
            
            msg.attach(text_part)
            msg.attach(html_part)
            
            with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
                server.starttls()
                server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email} via SMTP")
            return True
        except Exception as e:
            logger.error(f"Error sending email via SMTP: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using the configured method (SendGrid preferred, SMTP fallback)"""
        if self.use_sendgrid:
            success = self.send_email_sendgrid(to_email, subject, html_content, text_content)
            if not success and settings.SMTP_HOST:
                logger.info("SendGrid failed, falling back to SMTP")
                return self.send_email_smtp(to_email, subject, html_content, text_content)
            return success
        else:
            return self.send_email_smtp(to_email, subject, html_content, text_content)
    
    def send_newsletter_confirmation(self, email: str) -> bool:
        """Send newsletter subscription confirmation email"""
        subject = "Welcome to the Newsletter!"
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #1f2937; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9fafb; }}
                    .footer {{ padding: 20px; text-align: center; color: #6b7280; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>Welcome to the Newsletter!</h1>
                    </div>
                    <div class="content">
                        <p>Thank you for subscribing to my newsletter! You'll now receive updates about:</p>
                        <ul>
                            <li>New blog posts and tech insights</li>
                            <li>Latest projects and developments</li>
                            <li>Industry trends and best practices</li>
                        </ul>
                        <p>I'm excited to share my knowledge and experiences with you!</p>
                    </div>
                    <div class="footer">
                        <p>Best regards,<br><strong>Tyler Webb</strong><br>Escalations Engineer at Verkada</p>
                    </div>
                </div>
            </body>
        </html>
        """
        text_content = f"""
        Welcome to the Newsletter!
        
        Thank you for subscribing to my newsletter! You'll now receive updates about:
        - New blog posts and tech insights
        - Latest projects and developments
        - Industry trends and best practices
        
        I'm excited to share my knowledge and experiences with you!
        
        Best regards,
        Tyler Webb
        Escalations Engineer at Verkada
        """
        
        return self.send_email(email, subject, html_content, text_content)
    
    def send_new_post_notification(self, subscribers: List[str], post_title: str, post_url: str) -> bool:
        """Send new post notification to all subscribers"""
        subject = f"New Blog Post: {post_title}"
        html_content = f"""
        <html>
            <head>
                <style>
                    body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                    .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                    .header {{ background-color: #1f2937; color: white; padding: 20px; text-align: center; }}
                    .content {{ padding: 20px; background-color: #f9fafb; }}
                    .button {{ display: inline-block; background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                    .footer {{ padding: 20px; text-align: center; color: #6b7280; font-size: 14px; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>New Blog Post Available!</h1>
                    </div>
                    <div class="content">
                        <p>A new blog post has been published: <strong>{post_title}</strong></p>
                        <p>I've shared some insights and experiences that I think you'll find valuable.</p>
                        <a href="{post_url}" class="button">Read the Full Post</a>
                        <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                        <p>{post_url}</p>
                    </div>
                    <div class="footer">
                        <p>Best regards,<br><strong>Tyler Webb</strong><br>Escalations Engineer at Verkada</p>
                    </div>
                </div>
            </body>
        </html>
        """
        text_content = f"""
        New Blog Post Available!
        
        A new blog post has been published: {post_title}
        
        I've shared some insights and experiences that I think you'll find valuable.
        
        Read the full post here: {post_url}
        
        Best regards,
        Tyler Webb
        Escalations Engineer at Verkada
        """
        
        success_count = 0
        total_count = len(subscribers)
        
        for subscriber_email in subscribers:
            if self.send_email(subscriber_email, subject, html_content, text_content):
                success_count += 1
            else:
                logger.error(f"Failed to send notification to {subscriber_email}")
        
        logger.info(f"Sent {success_count}/{total_count} new post notifications successfully")
        return success_count > 0


# Create global email service instance
email_service = EmailService() 