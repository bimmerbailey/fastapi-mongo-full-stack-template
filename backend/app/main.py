import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth, users
from app.config.logging import logger

from app.database.init_db import connect_to_mongo, close_mongo_connection

app = FastAPI()
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
app.include_router(auth.router)
app.include_router(users.router)
