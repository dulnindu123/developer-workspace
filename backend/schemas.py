from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class ProjectCreate(BaseModel):
    name: str
    description: Optional[str] = None
    language: str

class ProjectResponse(ProjectCreate):
    id: int
    owner_id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class NodeResponse(BaseModel):
    id: int
    name: str
    file_path: str
    start_line: int
    end_line: int

    class Config:
        from_attributes = True

class EdgeResponse(BaseModel):
    id: int
    source: str
    target: str
    type: str

    class Config:
        from_attributes = True

class ArchitectureGraph(BaseModel):
    classes: List[NodeResponse]
    functions: List[NodeResponse]
    dependencies: List[EdgeResponse]
