from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import database
from app.models import user as models
from app.schemas import user as schemas
from app.dependencies.auth import get_current_user
from app.crud import user as crud

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.create_user(db=db, user=user)
    if db_user is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_user

@router.get("/protected-route/")
def protected_route(current_user: models.User = Depends(get_current_user)):
    return {"message": f"Hello {current_user.email}!"}
