import os
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.config import settings
from app.config.logging import setup_fastapi, setup_logging
from app.database.init_db import close_mongo_connection, connect_to_mongo
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await connect_to_mongo()
    yield
    await close_mongo_connection(client)


def init_app():
    setup_logging(json_logs=settings.json_logs, log_level=settings.log_level)

    app = FastAPI(
        docs_url="/api/docs",
        redoc_url="/api/redoc",
        openapi_url="/api/openapi.json",
        lifespan=lifespan,
    )
    env = os.environ.get("ENV", "dev")

    if env != "dev":
        app = FastAPI(docs_url=None, redoc_url=None)

    origins = ["*"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_fastapi(app)
    app.include_router(auth_router)
    app.include_router(users_router)

    return app
