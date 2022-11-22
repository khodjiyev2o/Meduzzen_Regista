
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.models.workers import Worker

from app.models.users import User
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.future import select
from typing import Optional

from app.services.users import UserCRUD




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
                username=user.username,
                description=new_worker.description)

                