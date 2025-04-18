import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# Load environment variables from .env file
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

# connect_args for SQLite
engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread":False}
)

# SessionLocal instance for every DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to use for ORM models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        