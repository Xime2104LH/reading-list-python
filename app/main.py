from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db.database_setup import create_db_and_tables
from app.routers import auth, url

@asynccontextmanager
async def lifespan(api: FastAPI):
    print(" 🟢 Starting up")
    create_db_and_tables()
    yield
    print(" 🔴 Sutting down")

def get_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    app.include_router(auth.router)
    app.include_router(url.router)
    return app

app = get_app()