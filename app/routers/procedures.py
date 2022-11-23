from app.schemas.procedures import ProcedureAlterSchema, ProcedureCreateSchema, ProcedureSchema
from app.services.procedures import ProcedureCrud, get_procedure
from app.models.locations import Location
from app.models.users import User

from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

procedure_router = APIRouter(
    prefix="/procedures",
    tags=["procedures"],
    responses={404: {"description": "Not found"}},
)






@procedure_router.post('/add', response_model=ProcedureSchema)
async def add_procedure(procedure: ProcedureCreateSchema, session: AsyncSession = Depends(get_session)) -> ProcedureSchema:
    result = await ProcedureCrud(session=session).create_procedure(procedure=procedure)
    return result
