from pydantic import BaseModel
from typing import Optional

class CourseCreate(BaseModel):
    title: str
    description: str
    # instructor_id sera automatiquement assigné depuis l'utilisateur connecté

class CourseUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    instructor_id: Optional[int] = None

class CourseResponse(BaseModel):
    id: int
    title: str
    description: str
    instructor_id: int
    
    class Config:
        from_attributes = True

class CourseWithInstructor(BaseModel):
    id: int
    title: str
    description: str
    instructor_id: int
    instructor_name: str
    instructor_email: str
    
    class Config:
        from_attributes = True