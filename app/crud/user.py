from sqlalchemy.orm import Session
from app.models import user as models
from app.schemas import user as schemas
from app.utils import hash_password

# Create new user
def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        email=user.email,
        hashed_password=user.password
    )
    db_user = db.query(models.User).filter(models.User.email== user.email).first()
    
    # If there is no register email create a user
    if db_user is None:
        hashed_pw = hash_password(user.password)
        new_user = models.User(email=user.email, hashed_password=hashed_pw)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    # Returns None if there is already a register user
    return None  
    