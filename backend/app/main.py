from contextlib import asynccontextmanager
from typing import Sequence

import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.logging import setup_fastapi, setup_logging
from app.config.settings import AppSettings, get_app_settings
from app.dependencies.database import close_mongo_connection, connect_to_mongo
from app.routes.auth import router as auth_router
from app.routes.items import router as items_router
from app.routes.users import router as users_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    client = await connect_to_mongo()
    yield
    await close_mongo_connection(client)


def init_app(app_settings: AppSettings = get_app_settings()):
    log_renderer: Sequence[structlog.types.Processor]
    if app_settings.debug:
        log_renderer = [structlog.dev.ConsoleRenderer()]
    else:
        log_renderer = [
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ]
    log_level = "DEBUG" if app_settings.debug else "INFO"
    setup_logging(processors=log_renderer, log_level=log_level)

    app = FastAPI(
        root_path="/api",
        lifespan=lifespan,
        debug=True if app_settings.debug else False,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    setup_fastapi(app)
    app.include_router(auth_router)
    app.include_router(users_router)
    app.include_router(items_router)

    return app
