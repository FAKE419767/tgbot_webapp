from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database import get_session
from app.bll.user_service import UserService
from app.api.schemas.users import (
    UserCreate,
    UserUpdate,
    UserResponse
)


router = APIRouter()


def get_user_service(
    session: AsyncSession = Depends(get_session)
) -> UserService:
    return UserService(session)


@router.get("/", response_model=list[UserResponse])
async def get_users(
    service: UserService = Depends(get_user_service)
):
    return await service.get_all()


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    return await service.get_by_id(user_id)


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
    data: UserCreate,
    service: UserService = Depends(get_user_service)
):
    return await service.create(data)


@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    data: UserUpdate,
    service: UserService = Depends(get_user_service)
):
    return await service.update(user_id, data)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_user(
    user_id: int,
    service: UserService = Depends(get_user_service)
):
    await service.delete(user_id)
