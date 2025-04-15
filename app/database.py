from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker


# SQLite database URL 
SQLALCHEMY_DATABASE_URL = "sqlite:///./task_manager.db"

# connect_args for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread":False}
)

# SessionLocal instance for every DB session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class to use for ORM models
Base = declarative_base()
