#fonctions réutilisable pour l'auth de user

from datetime import datetime, timedelta
from jose import jwt, JWTError
from passlib.context import CryptContext

SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 1

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ========= Password hashing ===============
def hash_password(password: str):
  return pwd_context.hash(password)

# === verifying password ===
def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

# ==== JWT Token ====
def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  expire = datetime.now() + (expires_delta or timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS))
  to_encode.update({"exp": expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  
def decode_access_token(token: str):
  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    return payload
  except JWTError:
    return None
