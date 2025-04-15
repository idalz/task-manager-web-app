from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()

# Task class for Task model
class Task(Base):
    __tablename__  = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description  = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
