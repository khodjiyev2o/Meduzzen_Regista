from app.schemas.appointments import AppointmentAlterSchema, AppointmentCreateSchema, AppointmentSchema
from app.models.appointments import Appointment
from app.models.users import User
from app.services.appointments import AppointmentCRUD
from app.db import get_session
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.users import get_user

appointment_router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
    responses={404: {"description": "Not found"}},
)


# @user_router.get('/users/validate', response_model=UserSchema)
# async def validate(user: UserSchema = Depends(get_or_create_user)) -> UserSchema:
#     return user


@appointment_router.get('/all', response_model=list[AppointmentSchema])
async def all_appointments(session: AsyncSession = Depends(get_session), page: int = Query(default=1)) -> list[AppointmentSchema]:
    result = await AppointmentCRUD(session=session).get_all_appointments(page=page)
    return result


@appointment_router.get('/{id}', response_model=list[AppointmentSchema])
async def get_appointments_by_worker_id(worker_id: int, session: AsyncSession = Depends(get_session)) -> list[AppointmentSchema]:
    result = await AppointmentCRUD(session=session).get_appointments_for_worker(worker_id=worker_id)
    return result


@appointment_router.post('/add', response_model=AppointmentSchema)
async def add_appoinment(appointment: AppointmentCreateSchema, session: AsyncSession = Depends(get_session)) -> AppointmentSchema:
    result = await AppointmentCRUD(session=session).create_appoinment(appointment=appointment)
    return result

@appointment_router.delete('/delete')
async def cancel_appoinment(appointment_id: int,session: AsyncSession = Depends(get_session),user: User = Depends(get_user)) -> AppointmentSchema:
    if user.admin:
        result = await AppointmentCRUD(session=session).delete_appointment(appointment_id=appointment_id)
        return result
    else:
        raise HTTPException(403,"You are not an admin!")

