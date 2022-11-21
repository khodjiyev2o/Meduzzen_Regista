from app.schemas.users import UserCreateSchema, UserLoginSchema, UserSchema, UserAlterSchema
from app.models.workers import Worker
from app.models.users import User
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.services.workers import WorkerCRUD
from app.db import get_session
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

worker_router = APIRouter(
    prefix="/workers",
    tags=["workers"],
    responses={404: {"description": "Not found"}},
)


# @user_router.get('/users/validate', response_model=UserSchema)
# async def validate(user: UserSchema = Depends(get_or_create_user)) -> UserSchema:
#     return user


# @user_router.get('/all', response_model=list[UserSchema])
# async def all_users(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[UserSchema]:
#     result = await UserCRUD(session=session).get_users(page)
#     return result


@worker_router.post('/add', response_model=WorkerSchema)
async def add_company(
            worker: WorkerCreateSchema, 
            session: AsyncSession = Depends(get_session), 
            user: User = Depends(get_user)) -> WorkerSchema:

    worker = await WorkerCRUD(session=session).create_worker(worker=worker, user=user)
    return worker