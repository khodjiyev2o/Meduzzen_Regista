from app.schemas.users import UserCreateSchema, UserLoginSchema, UserSchema, UserAlterSchema
from app.models.workers import Worker
from app.models.users import User
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.services.workers import WorkerCRUD, get_worker
from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

worker_router = APIRouter(
    prefix="/workers",
    tags=["workers"],
    responses={404: {"description": "Not found"}},
)


@worker_router.get('/all', response_model=list[WorkerSchema])
async def all_workers(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[WorkerSchema]:
    workers = await WorkerCRUD(session=session).get_workers(page)
    return workers

@worker_router.post('/add')
async def add_worker(
            worker: WorkerCreateSchema, 
            session: AsyncSession = Depends(get_session), 
            user: User = Depends(get_user)) -> WorkerSchema:

    if user.admin:
        result = await WorkerCRUD(session=session).create_worker(worker=worker)
        return result


@worker_router.patch('/patch', response_model=WorkerSchema)
async def patch_worker(worker: WorkerAlterSchema,user: User = Depends(get_user), db_worker: Worker = Depends(get_worker)) -> WorkerSchema:
    if user.admin:
        worker = await WorkerCRUD(worker=db_worker).patch_worker(worker=worker)
        return worker
    raise HTTPException(403,f"This user is not autharized to update a worker")


@worker_router.delete('/delete')
async def delete_worker(worker_id: int,user: User = Depends(get_user)) -> HTTPException:
    if user.admin:
        worker = await WorkerCRUD(user=user).delete_worker(worker_id=worker_id)
        return worker
    raise HTTPException(403,f"This user is not autharized to delete a worker")



