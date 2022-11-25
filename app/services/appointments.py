from app.models.appointments import Appointment
from app.models.schedules import Schedule
from app.services.schedules import ScheduleCrud
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from fastapi import HTTPException, Header, Depends
from app.schemas.appointments import AppointmentAlterSchema, AppointmentCreateSchema, AppointmentSchema
from passlib.hash import pbkdf2_sha256 as sha256
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params
from app.db import get_session

from typing import Optional






class AppointmentCRUD:
    def __init__(self, session: Optional[AsyncSession] = None, appointment: Optional[Appointment] = None):
        if not session:
            self.session = async_object_session(appointment)
        else:
            self.session = session
        self.appointment = appointment

    async def create_appoinment(self, appointment: AppointmentCreateSchema) -> AppointmentSchema:
        db_appointment = await self.session.execute(select(Appointment).filter(and_(
            Appointment.worker_id == appointment.worker_id,
             Appointment.user_id == appointment.user_id,
             Appointment.date == appointment.date,
              Appointment.start_time == appointment.start_time
             )))
        db_appointment = db_appointment.scalars().first()
        if db_appointment:
            ## checks for similar appointments
            raise HTTPException(404, 'You have already been appointment to this worker')
        ## get worker schedule 
        worker_schedules =  await ScheduleCrud(session=self.session).get_schedule_for_worker(worker_id=appointment.worker_id)
        for worker_schedule in worker_schedules:
            ## check if this worker is available at user appointed time , 1)worker does not work at this time 2) other users might reserve the place
            available = await self.worker_is_available(worker_schedule=worker_schedule,appointment=appointment)    
            if available:
                new_appointment = Appointment(user_id=appointment.user_id,
                                                worker_id=appointment.worker_id,
                                                date=appointment.date, 
                                                start_time=appointment.start_time,
                                                end_time=appointment.end_time,
                                                procedure_id=appointment.procedure_id)
                self.session.add(new_appointment)
                await self.session.commit()
                return AppointmentSchema(id=new_appointment.id,
                                    user_id=appointment.user_id,
                                    worker_id=appointment.worker_id,
                                    date=appointment.date, 
                                    start_time=appointment.start_time, 
                                    end_time=appointment.end_time,
                                    procedure_id=appointment.procedure_id)


    async def delete_appointment(self, appointment_id: int) -> HTTPException:
        appointment_tobe_deleted = await self.session.get(Appointment,appointment_id)
        if appointment_tobe_deleted:
            await self.session.delete(appointment_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Appointment with id {appointment_tobe_deleted.id} is successfully deleted")
        raise HTTPException(404,f"Appoinment with this id  not found")

    
    async def get_all_appointments(self, page: int) -> list[AppointmentSchema]:
        params = Params(page=page, size=10)
        appointments = await paginate(self.session, select(Appointment), params=params)
        return [AppointmentSchema(id=appointment.id,
                                    user_id=appointment.user_id,
                                    worker_id=appointment.worker_id,
                                    date=appointment.date,
                                    start_time=appointment.start_time, 
                                    end_time=appointment.end_time,
                                    procedure_id=appointment.procedure_id) for appointment in appointments.items]


    async def get_appointments_for_worker(self,worker_id):
        appointments = await self.session.execute(select(Appointment).filter(Appointment.worker_id == worker_id))
        return [AppointmentSchema(id=appointment[0].id,
                                user_id=appointment[0].user_id,
                                worker_id=appointment[0].worker_id,
                                date=appointment[0].date, 
                                start_time=appointment[0].start_time,
                                end_time=appointment[0].end_time,
                                procedure_id=appointment[0].procedure_id) for appointment in appointments]


    ## Это функция проперает совпадает ли время юзера и время работы специалиста 
    async def  worker_is_available(self,worker_schedule,appointment):
        if worker_schedule.date == appointment.date and worker_schedule.start_time <= appointment.start_time and  worker_schedule.end_time >= appointment.end_time:
           print(f"Worker is working in {appointment.start_time} to {appointment.end_time}")
           print(f"Let's check if there is someone has already reserved this time")
           no_appoinment = await self.worker_has_not_appointments(worker_schedule=worker_schedule,appointment=appointment)
           return True
        elif worker_schedule.date == appointment.date and worker_schedule.start_time >= appointment.start_time and  worker_schedule.end_time <= appointment.end_time:
            print("Running 2nd condition....")
            await self.worker_has_not_appointments(worker_schedule=worker_schedule,appointment=appointment)
            return True
        elif worker_schedule.date == appointment.date and  worker_schedule.start_time > appointment.start_time and  worker_schedule.end_time > appointment.end_time:
            await self.worker_has_not_appointments(worker_schedule=worker_schedule,appointment=appointment)
            return True
        else:    
            return False
        
       

       
       

    ## Эта функция проверяет нет ли у специалиста, такие ж записи как у данного юзера(т.е Никто ли не записан на это время к нему на осмотр)
    async def worker_has_not_appointments(self,worker_schedule,appointment):
        db_worker_appointments = await self.get_appointments_for_worker(worker_id=worker_schedule.worker_id)
        print("Running 2nd function of a worker....")
        if db_worker_appointments:
            for db_worker_appointment in db_worker_appointments:
                print("Running loop of 2nd  function....")
                if db_worker_appointment.date == appointment.date and db_worker_appointment.start_time <= appointment.start_time and db_worker_appointment.end_time >= appointment.end_time:
                        print("Running  1st  condintion of 2 function....")
                        raise HTTPException(403,f"Worker has other appointments from  {db_worker_appointment.start_time} to {db_worker_appointment.end_time}!")
                elif db_worker_appointment.date == appointment.date and db_worker_appointment.start_time >= appointment.start_time and db_worker_appointment.end_time <= appointment.end_time :
                        raise HTTPException(403,f"2Worker has other appointments from  {db_worker_appointment.start_time} to {db_worker_appointment.end_time}!")
        else:
            print("RETURNING TRUE...")
            return True
        