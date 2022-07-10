from datetime import timedelta, datetime

from fastapi import HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from core.configs import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, BANNED
from core.models.admin.users.admin_users_methods import unban_user
from core.models.user.user_methods import get_user
from core.schemas import UserAbstractModel
from core.store import UserTable

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


def is_user_banned(user: UserTable) -> bool:
    if user.state == BANNED:
        return True
    return False


def is_ban_date_expired(user: UserTable) -> bool:
    current_date = datetime.now()
    if current_date >= user.ban_term:
        return True
    return False


def check_ban_data(user: UserTable, session: Session) -> None:
    if is_user_banned(user):
        if is_ban_date_expired(user):
            unban_user(user, session)
            return
        raise HTTPException(status_code=403, detail=f"You are banned till {user.ban_term}")
