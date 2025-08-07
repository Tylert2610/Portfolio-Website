from pydantic import BaseModel, EmailStr
from typing import Optional


class NewsletterSubscription(BaseModel):
    """Schema for newsletter subscription requests"""

    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
