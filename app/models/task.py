from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


# Task class for Task model
class Task(Base):
    __tablename__  = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=True)
    description  = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="tasks")
