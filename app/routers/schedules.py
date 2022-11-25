from app.schemas.schedules import ScheduleAlterSchema, ScheduleCreateSchema, ScheduleSchema
from app.services.schedules import ScheduleCrud, get_schedule
from app.models.schedules import Schedule
from app.models.users import User

from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

schedule_router = APIRouter(
    prefix="/schedules",
    tags=["schedules"],
    responses={404: {"description": "Not found"}},
)






@schedule_router.post('/add', response_model=ScheduleSchema)
async def add_schedules(schedule: ScheduleCreateSchema, session: AsyncSession = Depends(get_session)) -> ScheduleSchema:
    result = await ScheduleCrud(session=session).create_schedule(schedule=schedule)
    return result


@schedule_router.get('/all', response_model=list[ScheduleSchema])
async def all_schedules(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[ScheduleSchema]:
    result = await ScheduleCrud(session=session).get_schedules(page)
    return result

@schedule_router.get('/of_worker', response_model=list[ScheduleSchema])
async def all_schedules_of_worker(worker_id: int,session: AsyncSession = Depends(get_session)) -> list[ScheduleSchema]:
    result = await ScheduleCrud(session=session).get_schedule_for_worker(worker_id=worker_id)
    return result


@schedule_router.delete('/delete')
async def delete_schedules(schedule_id: int,user: User = Depends(get_user), schedule: Schedule = Depends(get_schedule)) -> HTTPException:
    if user.admin:
        result = await ScheduleCrud(schedule=schedule).delete_schedule(schedule_id=schedule_id)
        return result
    raise HTTPException(403,f"This user is not autharized to delete a schedule")