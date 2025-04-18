from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Task class for Task model
class Task(Base):
    __tablename__  = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description  = Column(String, nullable=True)
    status = Column(String, default="pending")
    due_date = Column(DateTime, nullable=True)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
