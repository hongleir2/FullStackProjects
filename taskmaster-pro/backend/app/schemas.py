from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

# Pydantic models validate, parse, and convert data based on type hints, ensuring consistent, structured, and reliable data handling in Python applications.

# Pydantic models are defined by creating a class that inherits from Pydantic's BaseModel class.
class UserCreate(BaseModel):
    email: EmailStr
    password: str

# This is the Pydantic model for the User object. 
# It is used to define the schema for the User object that will be used in the API.
class User(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    class Config:
        orm_mode = True

# This is the Pydantic model for the Token object.
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[EmailStr] = None

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    is_completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    owner: User
    class Config:
        orm_mode = True