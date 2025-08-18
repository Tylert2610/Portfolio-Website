from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....core.email import email_service
from ....database import get_db
from ....schemas import NewsletterSubscription

router = APIRouter()


@router.post("/subscribe", response_model=dict)
async def subscribe_newsletter(
    subscription: NewsletterSubscription, db: Session = Depends(get_db)
):
    """Subscribe to newsletter using SendGrid subscription groups"""
    try:
        # Add to SendGrid subscription group (handles compliance automatically)
        success = email_service.add_to_subscription_group(
            email=subscription.email,
            first_name=getattr(subscription, "first_name", None),
            last_name=getattr(subscription, "last_name", None),
        )

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to subscribe to newsletter"
            )

        # Send confirmation email
        email_service.send_newsletter_confirmation(subscription.email)

        return {
            "message": "Successfully subscribed to newsletter",
            "email": subscription.email,
            "status": "active",
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription failed: {str(e)}")


@router.post("/unsubscribe")
async def unsubscribe_newsletter(
    subscription: NewsletterSubscription, db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter using SendGrid subscription groups"""
    try:
        # Remove from SendGrid subscription group
        success = email_service.remove_from_subscription_group(subscription.email)

        if not success:
            raise HTTPException(
                status_code=500, detail="Failed to unsubscribe from newsletter"
            )

        return {"message": "Successfully unsubscribed from newsletter"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unsubscribe failed: {str(e)}")


@router.get("/status/{email}")
async def get_subscription_status(email: str):
    """Get subscription status from SendGrid"""
    try:
        status = email_service.get_subscription_status(email)

        if status is None:
            raise HTTPException(
                status_code=500, detail="Failed to get subscription status"
            )

        return {"email": email, "status": status}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get status: {str(e)}")
