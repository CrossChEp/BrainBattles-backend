from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from starlette import status
from starlette.status import HTTP_401_UNAUTHORIZED

from core.configs import ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY, ALGORITHM
from core.middlewares.database_session import generate_session
from core.schemas import Token, TokenData, UserGetModel
from core.models import authenticate_user, get_user_by_id
from core.store import UserTable
from core.models.auth.auth_methods import create_access_token, check_ban_data

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")

auth_router = APIRouter()


def get_current_user(session: Session = Depends(generate_session), token: str = Depends(oauth2_scheme)):
    credetials_exception = HTTPException(
        status_code=HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        uid: int = payload.get('id')
        if uid is None:
            raise credetials_exception
        token_data = TokenData(id=uid)
    except JWTError:
        raise credetials_exception

    user = get_user_by_id(user_id=token_data.id, session=session)
    if user is None:
        raise credetials_exception
    check_ban_data(user, session)
    return user


@auth_router.post('/api/token', response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(generate_session)):
    user = authenticate_user(session=session, username=form_data.username,
                             password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(user.id)
    return Token(access_token=access_token, token_type='bearer')


@auth_router.get('/api/read/me', response_model=UserGetModel)
def read_user_me(current_user: UserTable = Depends(get_current_user)):
    return current_user
