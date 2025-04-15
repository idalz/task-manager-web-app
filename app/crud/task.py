from sqlalchemy.orm import Session
from app.models import task as models
from app.schemas import task as schemas


# Create a new task
def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        description=task.description,
        completed=task.completed
    )
    db.add(db_task) # Add the new task object to the session
    db.commit() # Save it in the DB
    db.refresh(db_task) # Give task an id from DB
    return db_task

# Get all tasks from the DB
def get_tasks(db: Session,  skip: int = 0, limit: int = 100):
    return db.query(models.Task).offset(skip).limit(limit).all()

# Get a single task by ID
def get_task(db: Session, task_id: int):
    return db.query(models.Task).filter(models.Task.id == task_id).first()
  