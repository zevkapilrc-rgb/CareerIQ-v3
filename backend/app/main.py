from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse

from .routes import (
    auth,
    resume,
    analytics,
    interview,
    learning_path,
    gamification,
    admin,
    chatbot,
    notifications,
    progress,
)
from .database import init_db

def create_app() -> FastAPI:
    app = FastAPI(title="CareerIQ API", version="1.0.0")

    # Enable CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Startup event
    @app.on_event("startup")
    async def on_startup():
        init_db()

    # Root endpoint
    @app.get("/", tags=["system"])
    async def root():
        return {"message": "CareerIQ Backend is running!", "version": "1.0.0"}

    # Health check endpoint
    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok"}

    # Optional redirect to Swagger UI
    @app.get("/docs-redirect", include_in_schema=False)
    async def docs_redirect():
        return RedirectResponse(url="/docs")

    # Include all routers
    app.include_router(auth.router, prefix="/auth", tags=["auth"])
    app.include_router(progress.router, prefix="/progress", tags=["progress"])
    app.include_router(resume.router, prefix="/resume", tags=["resume"])
    app.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
    app.include_router(interview.router, prefix="/interview", tags=["interview"])
    app.include_router(
        learning_path.router, prefix="/learning-path", tags=["learning-path"]
    )
    app.include_router(
        gamification.router, prefix="/gamification", tags=["gamification"]
    )
    app.include_router(admin.router, prefix="/admin", tags=["admin"])
    app.include_router(chatbot.router, prefix="/chatbot", tags=["chatbot"])
    app.include_router(notifications.router, prefix="/notifications", tags=["notifications"])

    @app.get("/check-keys", tags=["system"])
async def check_keys():
    import os

    openai_key = os.getenv("OPENAI_API_KEY")
    gemini_key = os.getenv("GEMINI_API_KEY")
    jwt_secret = os.getenv("JWT_SECRET")

    return {
        "OPENAI_KEY": bool(openai_key),
        "GEMINI_KEY": bool(gemini_key),
        "JWT_SECRET": bool(jwt_secret)
    }

    return app

# Create app instance
app = create_app()

