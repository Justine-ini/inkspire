from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import jwt
from src.config import config
import logging

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def generate_passwd_hash(plain_password: str) -> str:
    hashed_password = pwd_context.hash(plain_password)

    return hashed_password

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_data: dict, expire_delta: timedelta = None, refresh: bool = False) -> str:

    payload = {"sub": user_data.get("username")}
    payload['refresh'] = refresh
    
    if expire_delta:
        expire = datetime.now(timezone.utc) + expire_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=config.JWT_EXPIRATION_MINUTES)
    # payload.update({"exp": expire})
    payload.update({"exp": int(expire.timestamp())})
    token = jwt.encode(
        payload=payload,
        key=config.JWT_SECRET_KEY,
        algorithm=config.JWT_ALGORITHM
    )

    return token


def decode_access_token(token: str) -> dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token,
            key=config.JWT_SECRET_KEY,
            algorithms=[config.JWT_ALGORITHM]
        )
        return payload
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise credentials_exception
