from pydantic_settings import BaseSettings
from pydantic import field_validator, ConfigDict
from typing import Optional


class Settings(BaseSettings):
    # Database - Railway provides DATABASE_URL, local development uses individual components
    DATABASE_URL: Optional[str] = None

    # PostgreSQL specific settings (for local development/docker-compose)
    POSTGRES_DB: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None

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
    LOG_SQL_QUERIES: bool = False  # Set to True to see SQL queries in logs
    CORS_ORIGINS: str = (
        "http://localhost:3000,http://localhost:5173,http://localhost:4000,http://webbpulse.com,https://www.webbpulse.com"
    )

    @field_validator("CORS_ORIGINS")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse comma-separated CORS origins string into a list"""
        if isinstance(v, str):
            origins = [origin.strip() for origin in v.split(",") if origin.strip()]
            # Add localhost with different ports for development
            if "http://localhost:5173" in origins:
                origins.extend(
                    [
                        "http://localhost:3000",
                        "http://localhost:4000",
                        "http://127.0.0.1:5173",
                        "http://127.0.0.1:3000",
                        "http://127.0.0.1:4000",
                    ]
                )
            return list(set(origins))  # Remove duplicates
        return v

    model_config = ConfigDict(env_file=".env")

    def get_database_url(self) -> str:
        """Get database URL - prioritize DATABASE_URL (Railway) over individual components (local)"""
        if self.DATABASE_URL:
            return self.DATABASE_URL

        # Fall back to individual components for local development
        if all(
            [
                self.POSTGRES_DB,
                self.POSTGRES_USER,
                self.POSTGRES_PASSWORD,
                self.POSTGRES_HOST,
            ]
        ):
            return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:5432/{self.POSTGRES_DB}"

        raise ValueError(
            "Database configuration error: Either DATABASE_URL must be set (Railway) "
            "or all individual PostgreSQL components must be set (local development)"
        )


# Create settings instance
settings = Settings()
