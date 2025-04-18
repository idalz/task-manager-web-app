from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.schemas import task as schemas
from app.models import user as usermodels
from app.crud import task as crud
from app.dependencies import auth


router = APIRouter(prefix="/tasks", tags=["Tasks"])

# Create a new task
@router.post("/", response_model=schemas.TaskRead)
def create_task_route(
    task: schemas.TaskCreate,
    db: Session = Depends(database.get_db),
    current_user: usermodels.User = Depends(auth.get_current_user)
):    
    return crud.create_task(db=db, task=task, user=current_user)

# Update a task
@router.put("/{task_id}", response_model=schemas.TaskRead)
def update_task(
    task_id: int, 
    task: schemas.TaskUpdate, 
    db: Session = Depends(database.get_db),
    current_user: usermodels.User = Depends(auth.get_current_user)
):
    db_task = crud.update_task(db, task_id=task_id, task_update=task, user=current_user)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Delete a task
@router.delete("/{task_id}", response_model=schemas.TaskRead)
def delete_task(
    task_id: int, 
    db: Session = Depends(database.get_db),
    current_user: usermodels.User = Depends(auth.get_current_user)
):
    db_task = crud.delete_task(db, task_id=task_id, user=current_user)
    if  db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task

# Get all tasks
@router.get("/", response_model=list[schemas.TaskRead])
def  get_tasks(
    skip: int = 0, limit: int = 100, 
    db: Session = Depends(database.get_db),
    current_user: usermodels.User = Depends(auth.get_current_user)
):
    db_task = crud.get_tasks(db=db, skip=skip, limit=limit, user=current_user)
    if  db_task is None:
        raise HTTPException(status_code=404, detail="Tasks not found")
    return db_task
    
# Get a single task by ID
@router.get("/{task_id}", response_model=schemas.TaskRead) 
def get_task(
    task_id: int, 
    db: Session = Depends(database.get_db),
    current_user: usermodels.User = Depends(auth.get_current_user)   
):
    task = crud.get_task(db=db, task_id=task_id, user=current_user)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
