from datetime import timedelta

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from configs import ACCESS_TOKEN_EXPIRE_MINUTES
from schemas import Token, UserModel
from store import get_session, authenticate_user
from store.auth_methods import create_access_token, get_current_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

auth_router = APIRouter()


@auth_router.post('/token', response_model=Token)
def login_for_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    session: Session = Depends(get_session)):
    user = authenticate_user(session=session, nickname=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={'sub': user.nickname}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type='bearer')


@auth_router.get('/user/me', response_model=UserModel)
def read_user_me(current_user: UserModel = Depends(get_current_user)):
    return current_user