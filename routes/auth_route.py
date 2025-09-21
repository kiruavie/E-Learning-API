from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from schemas.user_schema import UserResponse, RegisterUser, LoginUser, TokenResponse
from db import get_session
from controllers import auth_controller

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def register(user: RegisterUser, db: Session = Depends(get_session)):
  try:
    return auth_controller.register(db, user)
  except ValueError as e:
    raise HTTPException(status_code=400, detail=str(e))

@router.post("/login", response_model=TokenResponse)
async def login(user: LoginUser, db: Session = Depends(get_session)):
  token =  auth_controller.authenticate_user(db, user.email, user.password)
  if not token:
    raise HTTPException(status_code=401, detail="Invalid credentials")
  return token