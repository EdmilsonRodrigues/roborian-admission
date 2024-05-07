from fastapi import FastAPI
from .routers.__init__ import api_router

app = FastAPI()

# Include API routers
app.include_router(api_router, prefix="/api", tags=["API"])

if __name__ == "__main__":
    import uvicorn

    # Run the FastAPI, application using uvicorn server
    uvicorn.run(app, host="127.0.0.1", port=8000)
