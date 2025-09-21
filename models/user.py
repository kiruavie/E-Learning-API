from sqlmodel import Field, SQLModel
from typing import Optional

class User(SQLModel, table=True):
  id: Optional[int]  = Field(default=None, primary_key=True, index=True)
  name: str
  email: str = Field(unique=True, index=True)
  password_hash: str
  role: str = Field(default="student") # instructor or student