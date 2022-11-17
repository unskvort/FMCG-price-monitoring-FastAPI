import os
from typing import Generator

import environ
import sentry_sdk
from fastapi import FastAPI
from passlib.context import CryptContext
from sqlmodel import Session, SQLModel, create_engine

env = environ.Env()
environ.Env.read_env(env_file="dev.env")
DATABASE_URL: str = os.environ.get("DATABASE_URL")  # type: ignore

engine = create_engine(DATABASE_URL, echo=False)

app = FastAPI(debug=os.environ.get("DEBUG"), version="0.0.1")  # type: ignore

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


sentry_sdk.init(
    dsn=os.environ.get("SENTRY_SDK_DSN"),
    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production,
    traces_sample_rate=1.0,
)


class ManageDB:
    @staticmethod
    def init_db() -> None:
        SQLModel.metadata.create_all(engine)

    @staticmethod
    def get_session() -> Generator:  # type: ignore
        with Session(engine) as session:
            yield session


db = ManageDB()
