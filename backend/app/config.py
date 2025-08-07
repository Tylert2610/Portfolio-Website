from pydantic_settings import BaseSettings
from pydantic import field_validator, ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Database - Use individual components with defaults for development
    DATABASE_URL: Optional[str] = None

    # PostgreSQL specific settings (for docker-compose)
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    # Security - Defaults for development
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # SendGrid (email service)
    SENDGRID_API_KEY: Optional[str] = None
    SENDGRID_FROM_EMAIL: str = "noreply@webbpulse.com"
    SENDGRID_FROM_NAME: str = "Tyler Webb Portfolio"
    SENDGRID_SUBSCRIPTION_GROUP_ID: Optional[str] = None

    # Application
    APP_NAME: str = "Portfolio Blog API"
    DEBUG: bool = False
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,https://webbpulse.com,https://www.webbpulse.com"
    )

    @field_validator("CORS_ORIGINS")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins string into a list"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = ConfigDict(env_file=".env")

    def get_database_url(self) -> str:
        """Construct database URL from individual components"""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"


# Create settings instance
settings = Settings()
