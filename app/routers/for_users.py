from app.schemas.appointments import AppointmentAlterSchema, AppointmentCreateSchema, AppointmentSchema
from app.schemas.workers import WorkerSchema
from app.services.workers import WorkerCRUD
from app.services.schedules import ScheduleCrud
from app.models.appointments import Appointment
from app.models.users import User
from app.services.appointments import AppointmentCRUD
from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user
from datetime import date, time

for_users_router = APIRouter(
    prefix="/for_users",
    tags=["for_users"],
    responses={404: {"description": "Not found"}},
)






#  список специалистов с возможностью фильтрации по их специальности

@for_users_router.get('/all_workers/by_specialization', response_model=list[WorkerSchema])
async def get_workers_by_specialization(specialization: str,session: AsyncSession = Depends(get_session)) -> list[WorkerSchema]:
    result = await WorkerCRUD(session=session).get_workers_by_specialization(specialization=specialization)
    return result


@for_users_router.get('/all_workers/by_location', response_model=list[WorkerSchema])
async def get_workers_for_one_location(location_id:int,session: AsyncSession = Depends(get_session)) -> list[WorkerSchema]:
    result = await WorkerCRUD(session=session).get_workers_for_one_location(location_id=location_id)
    return result


#API, позволяющее получить список специалистов, время приема специалиста для определенного дня 
@for_users_router.get('/all_workers/{date}', response_model=list[WorkerSchema])
async def get_workers_by_date(date:date,session: AsyncSession = Depends(get_session)) -> list[WorkerSchema]:
    result = await ScheduleCrud(session=session).get_workers_by_date(date=date)
    return result