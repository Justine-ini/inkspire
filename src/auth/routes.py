from fastapi import APIRouter, Depends, HTTPException, status
# from requests import session
from .schemas import UserCreateModel, UserModel, UserUpdateModel, UserLoginModel
from .service import UserService
from src.db.main import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from .utils import create_access_token, decode_access_token, verify_password
from datetime import timedelta
from fastapi.responses import JSONResponse


auth_router = APIRouter()
user_service = UserService()

RERESH_TOKEN_EXPIRY = 2


@auth_router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=UserModel)
async def create_user_Account(user_data: UserCreateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exist(email, session)
    if user_exists:
        raise HTTPException(status_code=400, detail="User with email already exists")
    created_user = await user_service.create_user(user_data, session)
    if not created_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User creation not successfull")
    return created_user

@auth_router.put('/user/update/{email}',status_code=status.HTTP_200_OK, response_model=UserModel)
async def update_user_Account(user_data: UserUpdateModel, session: AsyncSession = Depends(get_session)):
    email = user_data.email

    user_exists = await user_service.user_exist(email, session)
    if user_exists is None:
        raise HTTPException(status_code=400, detail="User with email does not exist")
    updated_user = await user_service.update_user(user_data, session)

    if not updated_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User update not successfull")
    return updated_user


@auth_router.get('/user/{email}', response_model=UserModel)
async def get_user_by_email(email: str, session: AsyncSession = Depends(get_session)):
    user = await user_service.get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@auth_router.post('/login')
async def login_user(login_data: UserLoginModel, session: AsyncSession = Depends(get_session)):
    try:
        email = login_data.email
        password = login_data.password

        user = await user_service.get_user_by_email(email, session)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        password_valid = verify_password(password, user.password)
        if not password_valid:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
        access_token = create_access_token(
            user_data = {
                'email': user.email,
                'user_uid':str(user.uid)
            }
        )
        refresh_token = create_access_token(
            user_data = {
                'email': user.email,
                'user_uid':str(user.uid)
            },
            refresh = True,
            expire_delta=timedelta(days=RERESH_TOKEN_EXPIRY)
        )

        return JSONResponse(
            content={
                "message":"Login Successful",
                "access_token":access_token,
                "refresh_token":refresh_token,
                "user":{
                    "email":user.email,
                    "uid":str(user.uid)
                }
            }
        )
    except Exception:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Email or Password")




