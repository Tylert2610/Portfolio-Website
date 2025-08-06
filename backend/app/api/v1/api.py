from fastapi import APIRouter
from .endpoints import posts, categories, subscribers, admin

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(posts.router, prefix="/posts", tags=["posts"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(subscribers.router, prefix="/subscribers", tags=["subscribers"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"]) 