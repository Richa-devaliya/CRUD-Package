# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.routes import users
from app.core.config import settings
from app.db import pg_session, mongo_session

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

@app.on_event("startup")
async def startup_event():
    """
    Initializes database connections on application startup.
    """
    if settings.DB_TYPE == "postgres":
        pg_session.init_db()
        print("Postgres DB Initialized")
    elif settings.DB_TYPE == "mongo":
        await mongo_session.init_db()
        print("MongoDB Initialized")

@app.on_event("shutdown")
async def shutdown_event():
    """
    Closes database connections on application shutdown.
    """
    if settings.DB_TYPE == "postgres":
        await pg_session.close_db()
        print("Postgres DB Connection Closed")
    elif settings.DB_TYPE == "mongo":
        await mongo_session.close_db()
        print("MongoDB Connection Closed")


app.include_router(users.router, prefix=settings.API_V1_STR, tags=["users"])

@app.get("/")
def read_root():
    """
    Root endpoint for health check.
    """
    return {"message": "API is running"}