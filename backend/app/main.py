"""Lucas & Olivia's Bedtime Storyteller – FastAPI application entry point."""

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import pathlib

from app.core.database import close_mongo_connection, connect_to_mongo
from app.routers import auth, dashboard, profiles, stories, voices


# ---------------------------------------------------------------------------
# Lifespan (replaces deprecated on_event startup/shutdown)
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Connect to MongoDB on startup and disconnect on shutdown."""
    await connect_to_mongo()
    yield
    await close_mongo_connection()


# ---------------------------------------------------------------------------
# Application factory
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Bedtime Storyteller API",
    description="Backend for Lucas & Olivia's Bedtime Storyteller iOS app.",
    version="1.0.0",
    lifespan=lifespan,
)

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Routers
# ---------------------------------------------------------------------------

API_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=API_PREFIX)
app.include_router(profiles.router, prefix=API_PREFIX)
app.include_router(stories.router, prefix=API_PREFIX)
app.include_router(dashboard.router, prefix=API_PREFIX)
app.include_router(voices.router, prefix=API_PREFIX)

# Serve generated audio files
_static_dir = pathlib.Path(__file__).parent.parent / "static"
_static_dir.mkdir(exist_ok=True)
((_static_dir / "audio")).mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(_static_dir)), name="static")


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------

@app.get("/health", tags=["health"])
async def health_check() -> dict:
    """Simple liveness probe."""
    return {"status": "ok", "service": "bedtime-storyteller-api"}
