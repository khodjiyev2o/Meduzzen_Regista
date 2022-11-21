from app.schemas.users import UserCreateSchema, UserLoginSchema, UserSchema, UserAlterSchema
from app.models.users import User
from app.services.users import UserCRUD
from app.db import get_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

user_router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# @user_router.get('/users/validate', response_model=UserSchema)
# async def validate(user: UserSchema = Depends(get_or_create_user)) -> UserSchema:
#     return user


@user_router.get('/all', response_model=list[UserSchema])
async def all_users(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[UserSchema]:
    result = await UserCRUD(session=session).get_users(page)
    return result


@user_router.get('/{id}', response_model=UserSchema)
async def get_user_by_id(id: int, session: AsyncSession = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session).get_user(id)
    return user


@user_router.post('/add', response_model=UserSchema)
async def add_user(user: UserCreateSchema, session: AsyncSession = Depends(get_session)) -> UserSchema:
    user = await UserCRUD(session=session).create_user(user)
    return user


@user_router.post('/login', response_model=str)
async def log_user(user: UserLoginSchema, session: AsyncSession = Depends(get_session)) -> str:
    token = await UserCRUD(session=session).login_user(user)
    return token


@user_router.patch('/patch', response_model=UserSchema)
async def patch_user(user: UserAlterSchema, db_user: User = Depends(get_user)) -> UserSchema:
    user = await UserCRUD(user=db_user).patch_user(user)
    return user


@user_router.delete('/deletes', response_model=UserSchema)
async def delete_user(user: User = Depends(get_user)) -> UserSchema:
    user = await UserCRUD(user=user).delete_user()
    return user