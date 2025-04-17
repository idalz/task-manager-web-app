from pydantic import BaseModel, EmailStr

# Base schema for shared fields
class UserBase(BaseModel):
    email: EmailStr

# Schema for creating a user
class UserCreate(UserBase):
    password: str

# Schema returned in responses (exclude password)
class UserRead(UserBase):
    id: int

    # Make it a response model
    class ConfigDict:
        from_attributes = True
        