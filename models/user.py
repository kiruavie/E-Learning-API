from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from .course import Course

class User(SQLModel, table=True):
  id: Optional[int]  = Field(default=None, primary_key=True, index=True)
  name: str
  email: str = Field(unique=True, index=True)
  password_hash: str
  role: str = Field(default="student") # instructor or student
  
  # Relation avec Course (pour les instructeurs)
  courses: List["Course"] = Relationship(back_populates="instructor")