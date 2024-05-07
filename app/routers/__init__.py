from fastapi import APIRouter
from .auth_routers import router as auth_router
from .user_router import router as user_router

# Create a new router instance
api_router = APIRouter()

# Include the API routers in the main router instance
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(user_router, prefix="/user", tags=["user"])
