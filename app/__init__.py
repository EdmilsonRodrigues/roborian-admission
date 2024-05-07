from fastapi import FastAPI
from .routers import api_router

# Create the FastAPI application instance
app = FastAPI()
app.include_router(api_router)

# Export the FastAPI application instance
__all__ = ['app']
