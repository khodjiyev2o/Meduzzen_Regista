
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


auth_cls = AuthHandler()


class ProcedureCrud:
    def __init__(self, session: Optional[AsyncSession] = None, procedure: Optional[Procedure] = None):
        if not session:
            self.session = async_object_session(procedure)
        else:
            self.session = session
        self.procedure = procedure

    async def create_procedure(self, procedure: ProcedureCreateSchema) -> Procedure:
        db_procedure = await self.session.execute(select(Procedure).filter(and_(Procedure.name == procedure.name,Procedure.duration == procedure.duration,Procedure.specialization == procedure.specialization)))
        db_procedure = db_procedure.scalars().first()
        if db_procedure:
            raise HTTPException(404, 'This procedure  already exists')
        else:
            new_procedure = Procedure(name=procedure.name, duration=procedure.duration, specialization=procedure.specialization,description=procedure.description)
            self.session.add(new_procedure)
            await self.session.commit()
            return Procedure(id=new_procedure.id, name=procedure.name, duration=procedure.duration, specialization=procedure.specialization, description=procedure.description)



async def get_procedure(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Procedure:
    if user.admin:
        procedure = await session.get(Procedure, id)
        if procedure:
                return procedure
        else:
            raise HTTPException(404, 'Procedure not found')
    raise HTTPException(404,"You are not authorized for this action!")