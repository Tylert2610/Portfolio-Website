from typing import Optional

from pydantic import BaseModel, EmailStr


class NewsletterSubscription(BaseModel):
    """Schema for newsletter subscription requests"""

    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
