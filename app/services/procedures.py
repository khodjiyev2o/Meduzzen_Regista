
from app.models.procedures import Procedure
from app.models.users import User
from app.services.users import get_user
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from fastapi import HTTPException, Header, Depends
from app.schemas.procedures import ProcedureAlterSchema, ProcedureCreateSchema, ProcedureSchema
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params
from app.db import get_session
from typing import Optional
from app.services.auth import AuthHandler
from app.services.workers import get_worker

auth_cls = AuthHandler()


class ProcedureCrud:
    def __init__(self, session: Optional[AsyncSession] = None, procedure: Optional[Procedure] = None):
        if not session:
            self.session = async_object_session(procedure)
        else:
            self.session = session
        self.procedure = procedure

    async def create_procedure(self, procedure: ProcedureCreateSchema) -> Procedure:
        db_procedure = await self.session.execute(select(Procedure).filter(and_(Procedure.worker_id == procedure.worker_id,Procedure.name == procedure.name,Procedure.duration == procedure.duration)))
        db_procedure = db_procedure.scalars().first()
        if db_procedure:
            raise HTTPException(404, 'This procedure  already exists')
        else:
            worker = get_worker(id=procedure.worker_id)
            new_procedure = Procedure(worker_id=procedure.worker_id,name=procedure.name, duration=procedure.duration,description=procedure.description)
            self.session.add(new_procedure)
            await self.session.commit()
            return Procedure(id=new_procedure.id,worker_id=procedure.worker_id, name=procedure.name, duration=procedure.duration,  description=procedure.description)

    async def get_procedures(self, page: int) -> list[ProcedureSchema]:
        params = Params(page=page, size=10)
        procedures = await paginate(self.session, select(Procedure), params=params)
        return [ProcedureSchema(id=procedure.id,worker_id=procedure.worker_id, name=procedure.name, duration=procedure.duration,description=procedure.description) for procedure in procedures.items]


    async def delete_procedure(self, procedure_id):
        procedure_tobe_deleted = await self.session.get(Procedure,procedure_id)
        if procedure_tobe_deleted:
            await self.session.delete(procedure_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Procedure with id {procedure_tobe_deleted.id} is successfully deleted")

async def get_procedure(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Procedure:
    if user.admin:
        procedure = await session.get(Procedure, id)
        if procedure:
                return procedure
        else:
            raise HTTPException(404, 'Procedure not found')
    raise HTTPException(404,"You are not authorized for this action!")