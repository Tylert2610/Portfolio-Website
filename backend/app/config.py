from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    # Database - No defaults for critical connection settings
    DATABASE_URL: str
    
    # PostgreSQL specific settings (for docker-compose)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    
    # Security - No defaults for authentication fields
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    
    # SendGrid (email service)
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
    
    def get_database_url(self) -> str:
        """Construct database URL from individual components"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"


# Create settings instance
settings = Settings() 