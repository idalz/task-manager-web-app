from sqlalchemy.orm import Session
from app.models import task as models
from app.models import user as usermodels
from app.schemas import task as schemas


# Create a new task 
def create_task(db: Session, task: schemas.TaskCreate, user: usermodels.User):
    db_task = models.Task(
        **task.model_dump(),
        owner_id=user.id
    )
    db.add(db_task) # Add the new task object to the session
    db.commit() # Save it in the DB
    db.refresh(db_task) # Give task an id from DB
    return db_task

# Update a task
def update_task(db: Session, task_id: int, task_update: schemas.TaskUpdate, user: usermodels.User):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()
    if db_task:
        db_task.title = task_update.title
        db_task.description = task_update.description
        db.commit() 
        db.refresh(db_task)
    return db_task

# Delete a task
def delete_task(db: Session, task_id: int, user: usermodels.User):
    db_task = db.query(models.Task).filter(
        models.Task.id == task_id,
        models.Task.owner_id == user.id
    ).first()
    if db_task:
        db.delete(db_task)
        db.commit()
    return db_task

# Get all tasks from the DB
def get_tasks(db: Session, user: usermodels.User, skip: int = 0, limit: int = 100):
    db_task = db.query(models.Task).filter(models.Task.owner_id == user.id).offset(skip).limit(limit).all()
    return db_task

# Get a single task by ID
def get_task(db: Session, task_id: int, user: usermodels.User):
    return db.query(models.Task).filter(models.Task.id == task_id, models.Task.owner_id == user.id).first()
