from pydantic import BaseModel # BaseModel is the base class for data validation and serialization in FastAPI.  Ensure the data coming into your API is correct and structured.
from typing import Optional #allows a field to be nullable or optional.
from datetime import datetime

# What the user sends when CREATING a task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None

# What the user sends when UPDATING a task 
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None

# What the API sends BACK
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    is_completed: bool
    created_at: datetime

    class Config:
        from_attributes = True  # allows converting SQLAlchemy model → PydanticS
        #Normally, Pydantic expects a dictionary, but with from_attributes=True, you can pass a SQLAlchemy object and it will automatical
        # ly convert it to a Pydantic response.

        