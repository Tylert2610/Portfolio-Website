from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class SubscriberBase(BaseModel):
    email: EmailStr


class SubscriberCreate(SubscriberBase):
    pass


class SubscriberUpdate(BaseModel):
    status: Optional[str] = None


class Subscriber(SubscriberBase):
    id: int
    status: str
    subscribed_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class NewsletterSubscription(BaseModel):
    email: EmailStr 