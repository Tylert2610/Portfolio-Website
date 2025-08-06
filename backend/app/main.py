from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .config import settings
from .database import init_db, test_db_connection

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Blog API for Portfolio Website",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
from .api.v1.api import api_router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    logger.info("Starting Portfolio Blog API...")
    
    # Test database connection
    if test_db_connection():
        # Initialize database tables
        init_db()
        logger.info("Database initialized successfully")
    else:
        logger.error("Failed to connect to database. Please check your database configuration.")


@app.get("/")
async def root():
    return {"message": "Portfolio Blog API", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    db_status = "healthy" if test_db_connection() else "unhealthy"
    return {
        "status": "healthy",
        "database": db_status,
        "version": "1.0.0"
    } 