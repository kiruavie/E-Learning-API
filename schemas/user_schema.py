from pydantic import BaseModel

class RegisterUser(BaseModel):
  name: str
  email: str
  password: str
  role: str
  
class LoginUser(BaseModel):
  email: str
  password: str

class TokenResponse(BaseModel):
  access_token: str
  token_type: str
  
class UserResponse(BaseModel):
  name: str
  email: str
  role: str
  
  class Config:
    from_attributes = True