
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.models.workers import Worker

from app.models.users import User
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.future import select
from typing import Optional
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from app.services.users import UserCRUD




class WorkerCRUD:
    def __init__(self, session: Optional[AsyncSession] = None, user: Optional[User] = None):
        if not session:
            self.session = async_object_session(user)
        else:
            self.session = session
        self.user = user

    async def create_worker(self, worker: WorkerCreateSchema) -> WorkerSchema:
        db_worker = await self.session.execute(select(Worker).filter(Worker.user_id == worker.user_id))
        db_worker = db_worker.scalars().first()
        if db_worker:
            raise HTTPException(404, 'worker already exists')
        else:
            new_worker = Worker(
                specialization=worker.specialization, 
                user_id=worker.user_id, 
                description=worker.description, 
            )


            self.session.add(new_worker)
            await self.session.commit()
            user = await UserCRUD(session=self.session).get_user(id=worker.user_id)
            return WorkerSchema(
                id=new_worker.id,
                specialization=new_worker.specialization,
                user_id=user.id,
                description=new_worker.description)

    
    async def get_workers(self, page: int) -> list[WorkerSchema]:
        params = Params(page=page, size=10)
        workers = await paginate(self.session, select(Worker), params=params)
        return [WorkerSchema(id=worker.id, user_id=worker.user_id, specialization=worker.specialization, description=worker.description,) for worker in workers.items]


    async def delete_worker(self, worker_id):
        worker_tobe_deleted = await self.session.get(Worker,worker_id)
        if worker_tobe_deleted:
            await self.session.delete(worker_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Worker with id {worker_tobe_deleted.id} is successfully deleted")
        raise HTTPException(404,f"Worker with id {id} not found")


    

                