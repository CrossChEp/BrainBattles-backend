from datetime import timedelta, datetime

from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES
from core.models.user.user_methods import get_user
from core.schemas import UserAbstractModel

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password_hash(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password(password):
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str):
    user = get_user(user=UserAbstractModel(nickname=username), session=session)
    if not user:
        return False
    if not verify_password_hash(password, user.password):
        return False
    return user


def create_access_token(uid: int):
    to_encode = {'id': uid}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
