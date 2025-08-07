from typing import List, Optional, Dict, Any
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (
    Mail,
    Email,
    To,
    Content,
    HtmlContent,
    PlainTextContent,
)
from ..config import settings
import logging

# Set up logging
logger = logging.getLogger(__name__)


class EmailService:
    def __init__(self):
        self.from_email = settings.SENDGRID_FROM_EMAIL
        self.from_name = settings.SENDGRID_FROM_NAME
        self.subscription_group_id = getattr(
            settings, "SENDGRID_SUBSCRIPTION_GROUP_ID", None
        )

        # Initialize SendGrid if API key is provided
        if settings.SENDGRID_API_KEY:
            self.sendgrid_client = SendGridAPIClient(api_key=settings.SENDGRID_API_KEY)
            self.use_sendgrid = True
            logger.info("SendGrid email service initialized")
        else:
            self.use_sendgrid = False
            logger.warning(
                "SendGrid API key not provided - email functionality disabled"
            )

    def add_to_subscription_group(
        self, email: str, first_name: str = None, last_name: str = None
    ) -> bool:
        """Add email to SendGrid subscription group"""
        try:
            # Use SendGrid's Marketing API to add to subscription group
            # This automatically handles compliance and unsubscribe management

            contact_data = {
                "contacts": [
                    {"email": email, "first_name": first_name, "last_name": last_name}
                ],
                "list_ids": (
                    [self.subscription_group_id] if self.subscription_group_id else []
                ),
            }

            response = self.sendgrid_client.client.marketing.contacts.put(
                request_body=contact_data
            )

            if response.status_code in [200, 201, 202]:
                logger.info(f"Successfully added {email} to subscription group")
                return True
            else:
                logger.error(
                    f"Failed to add to subscription group: {response.status_code} - {response.body}"
                )
                return False

        except Exception as e:
            logger.error(f"Error adding to subscription group: {e}")
            return False

    def remove_from_subscription_group(self, email: str) -> bool:
        """Remove email from SendGrid subscription group"""
        try:
            # Use SendGrid's Marketing API to remove from subscription group

            contact_data = {
                "contacts": [{"email": email}],
                "list_ids": [],  # Empty list removes from all groups
            }

            response = self.sendgrid_client.client.marketing.contacts.put(
                request_body=contact_data
            )

            if response.status_code in [200, 201, 202]:
                logger.info(f"Successfully removed {email} from subscription group")
                return True
            else:
                logger.error(
                    f"Failed to remove from subscription group: {response.status_code} - {response.body}"
                )
                return False

        except Exception as e:
            logger.error(f"Error removing from subscription group: {e}")
            return False

    def get_subscription_status(self, email: str) -> Optional[str]:
        """Get subscription status from SendGrid"""
        try:
            # Use SendGrid's Marketing API to check contact status
            response = self.sendgrid_client.client.marketing.contacts.search.post(
                request_body={"query": f"email = '{email}'"}
            )

            if response.status_code == 200:
                data = response.body
                if data.get("contact_count", 0) > 0:
                    contact = data["result"][0]
                    # Check if contact is in our subscription group
                    if (
                        self.subscription_group_id
                        and self.subscription_group_id in contact.get("list_ids", [])
                    ):
                        return "active"
                    else:
                        return "unsubscribed"
                else:
                    return "not_found"
            else:
                logger.error(
                    f"Failed to get subscription status: {response.status_code}"
                )
                return None

        except Exception as e:
            logger.error(f"Error getting subscription status: {e}")
            return None

    def send_email_sendgrid(
        self, to_email: str, subject: str, html_content: str, text_content: str
    ) -> bool:
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
                logger.error(
                    f"SendGrid API error: {response.status_code} - {response.body}"
                )
                return False

        except Exception as e:
            logger.error(f"Error sending email via SendGrid: {e}")
            return False

    def send_template_email(
        self, to_email: str, template_id: str, dynamic_template_data: Dict[str, Any]
    ) -> bool:
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
                logger.info(
                    f"Template email sent successfully to {to_email} via SendGrid"
                )
                return True
            else:
                logger.error(
                    f"SendGrid API error: {response.status_code} - {response.body}"
                )
                return False

        except Exception as e:
            logger.error(f"Error sending template email via SendGrid: {e}")
            return False

    def send_email(
        self, to_email: str, subject: str, html_content: str, text_content: str
    ) -> bool:
        """Send email using SendGrid with custom content"""
        if self.use_sendgrid:
            return self.send_email_sendgrid(
                to_email, subject, html_content, text_content
            )
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
            # SendGrid will automatically add unsubscribe links
        }

        if self.use_sendgrid:
            return self.send_template_email(email, template_id, dynamic_template_data)
        else:
            logger.error("SendGrid API key not configured - cannot send email")
            return False

    def send_new_post_notification(self, post_title: str, post_url: str) -> bool:
        """Send notification to all subscribers about a new blog post using SendGrid's Marketing API"""
        try:
            # Use SendGrid's Marketing API to send to entire subscription group
            # This automatically handles unsubscribe compliance
            url = "https://api.sendgrid.com/v3/mail/batch"

            campaign_data = {
                "name": f"New Blog Post: {post_title}",
                "subject": f"New Blog Post: {post_title}",
                "list_ids": (
                    [self.subscription_group_id] if self.subscription_group_id else []
                ),
                "template_id": "d-new_post_notification_template_id",  # TODO: Replace with actual template ID
                "dynamic_template_data": {
                    "post_title": post_title,
                    "post_url": post_url,
                    "author_name": "Tyler Webb",
                    "author_title": "Escalations Engineer at Verkada",
                },
            }

            response = self.sendgrid_client.client.mail.batch.post(
                request_body=campaign_data
            )

            if response.status_code in [200, 201, 202]:
                logger.info(f"New post notification campaign created successfully")
                return True
            else:
                logger.error(
                    f"Failed to create campaign: {response.status_code} - {response.body}"
                )
                return False

        except Exception as e:
            logger.error(f"Error sending new post notification: {e}")
            return False


# Create global email service instance
email_service = EmailService()
