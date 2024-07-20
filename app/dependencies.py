from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import crud
from .database import get_db
from .auth import verify_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # 토큰 데이터 검증
    token_data = verify_token(token, credentials_exception)
    # 사용자 검색
    user = crud.get_user_by_country_name(db, country_name=token_data.country_name)
    if user is None:
        raise credentials_exception
    return user
