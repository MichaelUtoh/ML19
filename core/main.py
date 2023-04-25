import psycopg2
from decouple import config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_sqlalchemy import DBSessionMiddleware

from core.routers import accounts, uploads
from core.config.database import create_db_and_tables


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title="OSS")
    configure_static(app)
    create_db_and_tables()
    return app


app = FastAPI(title="AIML19")

origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = start_application()
app.add_middleware(DBSessionMiddleware, db_url=config("DATABASE_URL"))
app.include_router(accounts.router)
app.include_router(uploads.router)
