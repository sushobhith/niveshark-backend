from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel
from database import get_db
from models import User
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
from typing import Dict, Any
from logger import logger

import os
import jwt

load_dotenv()

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

# Create the APIRouter instance
router = APIRouter()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------------------------
# Pydantic Schemas
# ---------------------------
class SignUpRequest(BaseModel):
  username: str
  email: str
  password: str

class SignInRequest(BaseModel):
  username: str
  password: str

class AuthResponse(BaseModel):
  username: str
  message: str
  token: str

# ---------------------------
# Helper Functions
# ---------------------------
def hash_password(password: str) -> str:
  return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
  return pwd_context.verify(plain_password, hashed_password)

def generate_jwt_token(username: str, secret_key: str, algorithm:str) -> str:
  payload = {
      "username": username,
      "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
    }

  jwt_token = jwt.encode(payload, secret_key, algorithm=algorithm)
  return jwt.encode(payload, secret_key, algorithm=algorithm)

# ---------------------------
# Routes
# ---------------------------

@router.post("/signup", response_model=AuthResponse)
def sign_up(payload: SignUpRequest, db: Session = Depends(get_db)):
  logger.info(f"Signup attempt for username: {payload.username}")
  
  existing_user = db.query(User).filter(User.username == payload.username).first()
  if existing_user:
    logger.warning(f"Signup failed - username already exists: {payload.username}")
    raise HTTPException(
      status_code=status.HTTP_400_BAD_REQUEST,
      detail="Username already taken."
    )

  hashed_pw = hash_password(payload.password)

  new_user = User(
    username=payload.username,
    email=payload.email,
    password_hash=hashed_pw
  )
  db.add(new_user)
  db.commit()
  db.refresh(new_user)

  token_payload = generate_jwt_token(new_user.username)
  token = jwt.encode(token_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

  logger.info(f"Successfully created new user: {payload.username}")

  return AuthResponse(
    username=new_user.username,
    message="User created successfully.",
    token=token
  )

@router.post("/signin", response_model=AuthResponse)
def sign_in(payload: SignInRequest, db: Session = Depends(get_db)):

  user = db.query(User).filter(User.username == payload.username).first()
  if not user or not verify_password(payload.password, user.password_hash):
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Invalid username or password."
    )
  
  token = generate_jwt_token(user.username, JWT_SECRET_KEY, JWT_ALGORITHM)

  return AuthResponse(
    username=user.username,
    message="Sign in successful.",
    token=token
  )
