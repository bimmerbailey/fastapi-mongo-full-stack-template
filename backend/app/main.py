import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, users
from app.config.logging import setup_logging, setup_fastapi
from app.config.config import settings
from app.database.init_db import connect_to_mongo, close_mongo_connection

setup_logging(json_logs=settings.json_logs, log_level=settings.log_level)
app = FastAPI(
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
)
env = os.environ.get("ENV", "dev")

if env != "dev":
    app = FastAPI(docs_url=None, redoc_url=None)

origins = ["*"]

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
setup_fastapi(app)
app.include_router(auth.router)
app.include_router(users.router)
