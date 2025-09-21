
from sqlmodel import Session, select
from models.user import User
from schemas.user_schema import RegisterUser
from utils.auth import hash_password, verify_password, create_access_token


# create or register user
def register(db: Session, user: RegisterUser):
  
  # verifier si l'email existe déjà
  statement = select(User).where(User.email == user.email)
  existing_user = db.exec(statement).first()
  
  if existing_user:
    raise ValueError("Email déjà utilisé")
  
  # hasher le mot de passe
  hashed_pw = hash_password(password=user.password)
  
  # new user
  new_user = User(name=user.name, email=user.email, password_hash=hashed_pw, role=user.role)
  db.add(new_user)
  db.commit()
  db.refresh(new_user)
  return new_user

def authenticate_user(db: Session, email: str, password: str):
  statement = select(User).where(User.email == email)
  user = db.exec(statement).first()
  if not user or not verify_password(password, user.password_hash):
    return None
  token = create_access_token({"sub": user.email})
  return {"access_token": token, "token_type": "bearer"}