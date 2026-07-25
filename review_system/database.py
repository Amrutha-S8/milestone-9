"""
Database setup for StayZa Native Review System.
Uses SQLAlchemy with SQLite for persistence.
"""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

REVIEW_DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "review_data")
os.makedirs(REVIEW_DB_DIR, exist_ok=True)

DATABASE_URL = os.getenv(
    "REVIEW_DATABASE_URL",
    f"sqlite:///{os.path.join(REVIEW_DB_DIR, 'reviews.db')}"
)

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
