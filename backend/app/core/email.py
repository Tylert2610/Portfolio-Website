from typing import List, Optional, Dict, Any
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
            logger.warning("SendGrid API key not provided - email functionality disabled")
    
    def send_email_sendgrid(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SendGrid API with custom content"""
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
    
    def send_template_email(self, to_email: str, template_id: str, dynamic_template_data: Dict[str, Any]) -> bool:
        """Send email using SendGrid template"""
        try:
            from_email = Email(self.from_email, self.from_name)
            to_email_obj = To(to_email)
            
            # Create mail object with template
            mail = Mail(from_email, to_email_obj)
            mail.template_id = template_id
            mail.dynamic_template_data = dynamic_template_data
            
            # Send email
            response = self.sendgrid_client.send(mail)
            
            if response.status_code in [200, 201, 202]:
                logger.info(f"Template email sent successfully to {to_email} via SendGrid")
                return True
            else:
                logger.error(f"SendGrid API error: {response.status_code} - {response.body}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending template email via SendGrid: {e}")
            return False
    
    def send_email(self, to_email: str, subject: str, html_content: str, text_content: str) -> bool:
        """Send email using SendGrid with custom content"""
        if self.use_sendgrid:
            return self.send_email_sendgrid(to_email, subject, html_content, text_content)
        else:
            logger.error("SendGrid API key not configured - cannot send email")
            return False
    
    def send_newsletter_confirmation(self, email: str) -> bool:
        """Send newsletter subscription confirmation email using template"""
        # TODO: Replace with actual template ID when available
        template_id = "d-newsletter_confirmation_template_id"  # Placeholder
        
        dynamic_template_data = {
            "email": email,
            "name": "Subscriber",  # Could be personalized if name is collected
            "signup_date": "today",  # Could be actual date
            "unsubscribe_url": f"{settings.FRONTEND_URL}/unsubscribe?email={email}" if hasattr(settings, 'FRONTEND_URL') else "#"
        }
        
        if self.use_sendgrid:
            return self.send_template_email(email, template_id, dynamic_template_data)
        else:
            logger.error("SendGrid API key not configured - cannot send email")
            return False
    
    def send_new_post_notification(self, emails: List[str], post_title: str, post_url: str) -> bool:
        """Send notification to subscribers about a new blog post using template"""
        # TODO: Replace with actual template ID when available
        template_id = "d-new_post_notification_template_id"  # Placeholder
        
        dynamic_template_data = {
            "post_title": post_title,
            "post_url": post_url,
            "author_name": "Tyler Webb",
            "author_title": "Escalations Engineer at Verkada",
            "unsubscribe_url": "#"  # Could be personalized per subscriber
        }
        
        if not self.use_sendgrid:
            logger.error("SendGrid API key not configured - cannot send email")
            return False
        
        # Send to each subscriber
        success_count = 0
        for email in emails:
            # Add subscriber-specific data
            subscriber_data = dynamic_template_data.copy()
            subscriber_data["email"] = email
            subscriber_data["unsubscribe_url"] = f"{settings.FRONTEND_URL}/unsubscribe?email={email}" if hasattr(settings, 'FRONTEND_URL') else "#"
            
            if self.send_template_email(email, template_id, subscriber_data):
                success_count += 1
        
        logger.info(f"New post notification sent to {success_count}/{len(emails)} subscribers")
        return success_count == len(emails)


# Create global email service instance
email_service = EmailService() 