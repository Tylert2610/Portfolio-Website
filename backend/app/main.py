from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager
from .config import settings
from .database import run_migrations, test_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler for database initialization"""
    # Startup
    logger.info("Starting Portfolio Blog API...")

    # Test database connection
    if test_db_connection():
        # Run database migrations
        if run_migrations():
            logger.info("Database initialized successfully")
        else:
            logger.error("Failed to run database migrations")
    else:
        logger.error(
            "Failed to connect to database. Please check your database configuration."
        )

    yield

    # Shutdown (if needed)
    logger.info("Shutting down Portfolio Blog API...")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Blog API for Portfolio Website",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"],
    allow_headers=[
        "Accept",
        "Accept-Language",
        "Content-Language",
        "Content-Type",
        "Authorization",
        "X-Requested-With",
        "Origin",
        "Access-Control-Request-Method",
        "Access-Control-Request-Headers",
    ],
    expose_headers=["Content-Length", "Content-Type"],
    max_age=86400,  # Cache preflight requests for 24 hours
)

# Include API routes
from .api.v1.api import api_router

app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Portfolio Blog API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "healthy" if test_db_connection() else "unhealthy"
    return {"status": "healthy", "database": db_status, "version": "1.0.0"}
