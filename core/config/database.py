import cloudinary
from decouple import config
from sqlmodel import SQLModel, create_engine, Session


engine = create_engine(config("DATABASE_URL"))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
