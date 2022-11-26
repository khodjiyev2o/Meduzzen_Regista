
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.schemas.schedules import ScheduleCreateSchema, ScheduleAlterSchema
from app.models.workers import Worker
from app.models.users import User
from app.models.schedules import Schedule

from fastapi import HTTPException, Header, Depends
from app.db import get_session
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.future import select
from typing import Optional, Union
from fastapi_pagination import Params
from fastapi_pagination.ext.async_sqlalchemy import paginate
from app.services.users import UserCRUD, get_user
from sqlalchemy import and_, or_
from datetime import date, time


class WorkerCRUD:
    def __init__(self, session: Optional[AsyncSession] = None, worker: Optional[Worker] = None):
        if not session:
            self.session = async_object_session(worker)
        else:
            self.session = session
        self.worker = worker

    async def create_worker(self, worker: WorkerCreateSchema) -> WorkerSchema:
        db_worker = await self.session.execute(select(Worker).filter(Worker.user_id == worker.user_id))
        db_worker = db_worker.scalars().first()
        if db_worker:
            raise HTTPException(404, 'worker already exists')
        new_worker = Worker(
                specialization=worker.specialization, 
                user_id=worker.user_id, 
                location_id=worker.location_id,
                description=worker.description, 
            )
        self.session.add(new_worker)
        await self.session.commit()
        return WorkerSchema(id=new_worker.id,specialization=new_worker.specialization,location_id=new_worker.location_id,user_id=new_worker.user_id,description=new_worker.description)

    
    async def get_workers(self, page: int) -> list[WorkerSchema]:
        params = Params(page=page, size=10)
        workers = await paginate(self.session, select(Worker), params=params)
        return [WorkerSchema(id=worker.id, user_id=worker.user_id, specialization=worker.specialization, description=worker.description,location_id=worker.location_id,) for worker in workers.items]

    async def get_workers_by_specialization(self,specialization: str)->list[WorkerSchema]:
        print("specialization ", specialization)
        workers =  await self.session.execute(select(Worker).filter(Worker.specialization == specialization))
        return [WorkerSchema(id=worker[0].id, user_id=worker[0].user_id, specialization=worker[0].specialization, description=worker[0].description,location_id=worker[0].location_id) for worker in workers]



    async def delete_worker(self, worker_id):
        worker_tobe_deleted = await self.session.get(Worker,worker_id)
        if worker_tobe_deleted:
            await self.session.delete(worker_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Worker with id {worker_tobe_deleted.id} is successfully deleted")
        raise HTTPException(404,f"Worker with id {id} not found")

    async def patch_worker(self, worker: WorkerAlterSchema) -> WorkerSchema:
        if worker.location_id:
            await self.check_worker_location(worker=worker)
            self.worker.location_id = worker.location_id
        if worker.description:
            self.worker.description = worker.description
        await self.session.commit()
        return WorkerSchema(id=self.worker.id, user_id=self.worker.user_id, specialization=self.worker.specialization, description=worker.description)

    async def get_workers_for_one_location(self, location_id: int) -> list[WorkerSchema]:
        workers =  await self.session.execute(select(Worker).filter(Worker.location_id == location_id))
        print("location_id ", location_id)
        return [WorkerSchema(id=worker[0].id, user_id=worker[0].user_id, specialization=worker[0].specialization, description=worker[0].description,location_id=worker[0].location_id) for worker in workers]
  
    

    async def check_worker_location(self,worker) -> bool:
        db_worker = await self.session.execute(select(Worker).filter(and_(Worker.specialization == worker.specialization, Worker.location_id == worker.location_id)))
        db_worker = db_worker.scalars().first()
        if db_worker:
                    raise HTTPException(403,"Two workers with the same specialization cannot work in one location at the same time!")
        return True   

    
async def get_worker(id: int,session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Worker:
   if user.admin:
        worker = await session.get(Worker, id)
        if worker:
                return worker
        else:
            raise HTTPException(404, 'worker not found')
   raise HTTPException(404,"You are not authorized for this action!")
