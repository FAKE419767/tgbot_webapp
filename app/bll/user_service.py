from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from pwdlib import PasswordHash

from app.models.user import User
from app.api.schemas.users import UserCreate, UserUpdate


password_hash = PasswordHash.recommended()


class UserService:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def get_by_id(self, user_id: int):
        user = await self.session.get(User, user_id)

        if not user:
            raise HTTPException(404, "User not found")

        return user

    async def create(self, data: UserCreate):
        existing = await self.session.scalar(
            select(User).where(
                (User.email == data.email) |
                (User.username == data.username)
            )
        )

        if existing:
            raise HTTPException(409, "Email or username already exists")

        user = User(
            username=data.username,
            email=data.email,
            hashed_password=password_hash.hash(data.password)
        )

        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def update(self, user_id: int, data: UserUpdate):
        user = await self.get_by_id(user_id)

        for key, value in data.model_dump(
            exclude_unset=True
        ).items():
            setattr(user, key, value)

        await self.session.commit()
        await self.session.refresh(user)

        return user

    async def delete(self, user_id: int):
        user = await self.get_by_id(user_id)

        await self.session.delete(user)
        await self.session.commit()
