
from app.schemas.workers import WorkerAlterSchema, WorkerSchema, WorkerCreateSchema
from app.models.workers import Worker
from app.models.users import User
from fastapi import HTTPException, Header, Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from sqlalchemy.future import select
from typing import Optional




class WorkerCRUD:
    def __init__(self, session: Optional[AsyncSession] = None, worker: Optional[Worker] = None):
        if not session:
            self.session = async_object_session(worker)
        else:
            self.session = session
        self.worker = worker

    async def create_worker(self, worker: WorkerCreateSchema, user: User) -> WorkerSchema:
        db_worker = await self.session.execute(select(Worker).filter(Worker.user_id == user.id))
        db_worker = db_worker.scalars().first()
        if db_worker:
            raise HTTPException(404, 'worker already created')
        else:
            new_worker = Worker(
                specialization=worker.specialization, 
                user_id=user.id, 
                description=worker.description, 
            )

            self.session.add(new_worker)
            await self.session.commit()
            return WorkerSchema(
                id=new_worker.id,
                specialization=new_worker.specialization,
                user=user.username,
                description=new_worker.description)

                