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


@procedure_router.get('/all', response_model=list[ProcedureSchema])
async def all_procedures(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[ProcedureSchema]:
    result = await ProcedureCrud(session=session).get_procedures(page)
    return result





@procedure_router.delete('/delete')
async def delete_procedure(procedure_id: int,user: User = Depends(get_user), procedure: Location = Depends(get_procedure)) -> HTTPException:
    if user.admin:
        result = await ProcedureCrud(procedure=procedure).delete_procedure(procedure_id=procedure_id)
        return result
    raise HTTPException(403,f"This user is not autharized to delete a location")