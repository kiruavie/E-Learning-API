from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from .user import User

class Course(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    title: str = Field(index=True)
    description: str
    instructor_id: int = Field(foreign_key="user.id")
    
    # Relation avec User (instructor)
    instructor: Optional["User"] = Relationship(back_populates="courses")
