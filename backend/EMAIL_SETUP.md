# Email Service Setup - SendGrid Integration

This document explains how to set up and configure the email service using SendGrid for the Portfolio Blog API.

## Overview

The email service has been migrated from AWS SES to SendGrid for improved reliability, better deliverability, and easier management. SendGrid is now the primary email service with SMTP as a fallback option.

## Features

- **SendGrid Integration**: Primary email service with API-based sending
- **SMTP Fallback**: Backup email method for development and reliability
- **Professional Templates**: Beautiful HTML email templates for newsletter and blog notifications
- **Error Handling**: Comprehensive error handling and logging
- **Automatic Fallback**: Automatic fallback to SMTP if SendGrid fails

## Setup Instructions

### 1. SendGrid Account Setup

1. Create a SendGrid account at [sendgrid.com](https://sendgrid.com)
2. Verify your sender domain or use a verified sender email
3. Generate an API key with "Mail Send" permissions
4. Note your API key for configuration

### 2. Environment Configuration

Create a `.env` file in the `backend/` directory with the following variables:

```env
# SendGrid Configuration (Primary)
SENDGRID_API_KEY=your-sendgrid-api-key-here
SENDGRID_FROM_EMAIL=noreply@portfolio.webbpulse.com
SENDGRID_FROM_NAME=Tyler Webb Portfolio

# SMTP Configuration (Fallback)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Legacy (kept for compatibility)
EMAIL_FROM=noreply@portfolio.webbpulse.com
```

### 3. Domain Verification

For production use, verify your domain with SendGrid:

1. Go to SendGrid Settings → Sender Authentication
2. Choose "Domain Authentication" or "Single Sender Verification"
3. Follow the verification steps
4. Update `SENDGRID_FROM_EMAIL` to use your verified domain

### 4. Testing the Integration

Run the test script to verify everything is working:

```bash
cd backend
python test_email.py
```

The test script will:

- Check your configuration
- Send a newsletter confirmation email
- Send a new post notification email
- Send a custom test email

## Email Templates

### Newsletter Confirmation

- **Subject**: "Welcome to the Newsletter!"
- **Content**: Professional welcome message with styling
- **Features**: Responsive design, clear call-to-action

### New Post Notification

- **Subject**: "New Blog Post: [Post Title]"
- **Content**: Announcement with link to the new post
- **Features**: Styled button, fallback text link, professional footer

## API Usage

### Basic Email Sending

```python
from app.core.email import email_service

# Send a custom email
success = email_service.send_email(
    to_email="user@example.com",
    subject="Test Subject",
    html_content="<h1>Hello</h1><p>This is HTML content.</p>",
    text_content="Hello\n\nThis is plain text content."
)
```

### Newsletter Confirmation

```python
# Send newsletter confirmation
success = email_service.send_newsletter_confirmation("user@example.com")
```

### New Post Notification

```python
# Send notification to all subscribers
subscribers = ["user1@example.com", "user2@example.com"]
success = email_service.send_new_post_notification(
    subscribers=subscribers,
    post_title="My New Blog Post",
    post_url="https://portfolio.webbpulse.com/blog/my-new-post"
)
```

## Error Handling

The email service includes comprehensive error handling:

- **SendGrid API Errors**: Logged with status codes and response details
- **SMTP Errors**: Logged with specific error messages
- **Automatic Fallback**: If SendGrid fails, automatically tries SMTP
- **Success Tracking**: Logs successful email deliveries

## Monitoring and Analytics

SendGrid provides excellent analytics and monitoring:

- **Delivery Rates**: Track email delivery success
- **Open Rates**: Monitor email engagement
- **Click Rates**: Track link clicks in emails
- **Bounce Management**: Handle bounced emails automatically
- **Webhook Support**: Real-time delivery status updates

## Troubleshooting

### Common Issues

1. **API Key Issues**

   - Verify your SendGrid API key is correct
   - Ensure the API key has "Mail Send" permissions
   - Check if the API key is active

2. **Domain Verification**

   - Ensure your sender domain is verified in SendGrid
   - Check DNS records for domain authentication
   - Use a verified single sender email for testing

3. **Rate Limits**

   - SendGrid has rate limits based on your plan
   - Monitor your usage in the SendGrid dashboard
   - Implement rate limiting in your application if needed

4. **SMTP Fallback Issues**
   - Verify SMTP credentials are correct
   - Check if your email provider allows app passwords
   - Ensure SMTP port is not blocked by firewall

### Debug Mode

Enable debug logging by setting the log level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Migration from AWS SES

If migrating from AWS SES:

1. **Remove AWS Dependencies**: AWS SES configuration has been removed
2. **Update Environment**: Replace AWS credentials with SendGrid API key
3. **Test Thoroughly**: Use the test script to verify functionality
4. **Monitor Delivery**: Check SendGrid dashboard for delivery status

## Security Considerations

- **API Key Security**: Never commit API keys to version control
- **Environment Variables**: Use environment variables for sensitive data
- **Rate Limiting**: Implement appropriate rate limiting for email sending
- **Input Validation**: Validate email addresses before sending

## Support

For SendGrid-specific issues:

- [SendGrid Documentation](https://docs.sendgrid.com/)
- [SendGrid Support](https://support.sendgrid.com/)

For application-specific issues:

- Check the application logs
- Review the error handling in the email service
- Test with the provided test script
