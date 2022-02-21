from datetime import timedelta, datetime
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from starlette.status import HTTP_401_UNAUTHORIZED

import store
from configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import TokenData, UserModel
from models.user_methods import get_user


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password(password):
    return pwd_context.hash(password)


def authenticate_user(session: Session, nickname: str, password: str):
    user = get_user(user=UserModel(nickname=nickname), session=session)
    if not user:
        return False
    if not verify_password_hash(password, user.password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
