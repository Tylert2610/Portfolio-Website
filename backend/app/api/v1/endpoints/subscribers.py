from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....database import get_db
from ....models import Subscriber
from ....schemas import NewsletterSubscription, Subscriber as SubscriberSchema
from ....core.email import email_service

router = APIRouter()


@router.post("/subscribe", response_model=SubscriberSchema)
async def subscribe_newsletter(
    subscription: NewsletterSubscription,
    db: Session = Depends(get_db)
):
    """Subscribe to newsletter"""
    # Check if already subscribed
    existing_subscriber = db.query(Subscriber).filter(
        Subscriber.email == subscription.email
    ).first()
    
    if existing_subscriber:
        if existing_subscriber.status == "active":
            raise HTTPException(status_code=400, detail="Email already subscribed")
        else:
            # Reactivate subscription
            existing_subscriber.status = "active"
            db.commit()
            db.refresh(existing_subscriber)
            
            # Send confirmation email
            email_service.send_newsletter_confirmation(subscription.email)
            
            return existing_subscriber
    
    # Create new subscription
    new_subscriber = Subscriber(email=subscription.email, status="active")
    db.add(new_subscriber)
    db.commit()
    db.refresh(new_subscriber)
    
    # Send confirmation email
    email_service.send_newsletter_confirmation(subscription.email)
    
    return new_subscriber


@router.post("/unsubscribe")
async def unsubscribe_newsletter(
    subscription: NewsletterSubscription,
    db: Session = Depends(get_db)
):
    """Unsubscribe from newsletter"""
    subscriber = db.query(Subscriber).filter(
        Subscriber.email == subscription.email
    ).first()
    
    if not subscriber:
        raise HTTPException(status_code=404, detail="Subscriber not found")
    
    subscriber.status = "unsubscribed"
    db.commit()
    
    return {"message": "Successfully unsubscribed"} 