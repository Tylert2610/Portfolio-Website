from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./portfolio_blog.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Email
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@webbpulse.com"
    
    # SendGrid (primary email service)
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: str = "noreply@webbpulse.com"
    SENDGRID_FROM_NAME: str = "Tyler Webb Portfolio"
    
    # Application
    APP_NAME: str = "Portfolio Blog API"
    DEBUG: bool = False
    CORS_ORIGINS: list[str] = [
        "http://localhost:3000", 
        "http://localhost:5173",
        "https://webbpulse.com",
        "https://www.webbpulse.com"
    ]
    
    class Config:
        env_file = ".env"


settings = Settings() 