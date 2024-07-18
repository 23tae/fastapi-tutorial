from datetime import datetime, timedelta
from jose import JWTError, jwt
import os
from dotenv import load_dotenv
from .schemas import TokenData

load_dotenv()

JWT_ACCESS_SECRET = os.getenv("JWT_ACCESS_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
JWT_ACCESS_EXPIRE_MIN = int(os.getenv("JWT_ACCESS_EXPIRE_MIN"))


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=JWT_ACCESS_EXPIRE_MIN)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, JWT_ACCESS_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, JWT_ACCESS_SECRET, algorithms=[JWT_ALGORITHM])
        country_name: str = payload.get("sub")
        if country_name is None:
            raise credentials_exception
        token_data = TokenData(country_name=country_name)
    except JWTError:
        raise credentials_exception
    return token_data
