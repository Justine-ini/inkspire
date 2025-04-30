from fastapi import HTTPException
from .utils import generate_passwd_hash
from src.auth.schemas import UserCreateModel, UserUpdateModel
from .models import User
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlmodel import select


class UserService:
    async def get_user_by_email(self, email: str, session: AsyncSession) -> User:
        """
        Fetches a user from the database by email.
        """
        try:
            statement = select(User).where(User.email == email)
            result = await session.exec(statement)
            user = result.first()
            return user
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

        
    async def user_exist(self, email: str, session: AsyncSession):
        """
        Checks if a user exists in the database by email.
        """
        try:
            user = await self.get_user_by_email(email, session)
            return user is not None
            # return bool(user)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    async def create_user(self, user_data: UserCreateModel, session: AsyncSession) -> User:
        """
        Creates a new user in the database.
        """
        try:
            user_data_dict = user_data.model_dump()  # Ensure Pydantic v2 compatibility

            # Securely hash password first
            user_data_dict["password"] = generate_passwd_hash(user_data_dict["password"])

            new_user = User(**user_data_dict)
            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)
            return new_user

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        

    async def update_user(self, user_data: UserUpdateModel, session: AsyncSession):
        """
        Creates a new user in the database.
        """
        try:
            email = user_data.email
            user = await self.get_user_by_email(email, session)
            user_data_dict = user_data.model_dump() 

            for key, value in user_data_dict.items():
                setattr(user, key, value)
            
            session.add(user)
            await session.commit()
            await session.refresh(user)
            return user

        except Exception as e:
            await session.rollback()
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")