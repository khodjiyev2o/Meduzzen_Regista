
from app.models.schedules import Schedule
from app.models.users import User
from app.models.workers import Worker
from app.services.users import get_user
from sqlalchemy.future import select
from sqlalchemy import or_, and_
from fastapi import HTTPException, Header, Depends
from app.schemas.schedules import ScheduleAlterSchema, ScheduleCreateSchema, ScheduleSchema
from app.schemas.workers import WorkerSchema
from sqlalchemy.ext.asyncio import AsyncSession, async_object_session
from fastapi_pagination.ext.async_sqlalchemy import paginate
from fastapi_pagination import Params
from app.db import get_session
from typing import Optional, Union





class ScheduleCrud:
    def __init__(self, session: Optional[AsyncSession] = None, schedule: Optional[Schedule] = None):
        if not session:
            self.session = async_object_session(schedule)
        else:
            self.session = session
        self.schedule= schedule

    async def create_schedule(self, schedule: ScheduleCreateSchema) -> Schedule:
            await self.check_worker_schedule(schedule=schedule)
            workers =  await self.session.execute(select(Worker).filter(Worker.id == schedule.worker_id))
            for worker in workers:
                worker = WorkerSchema(id=worker[0].id, user_id=worker[0].user_id, specialization=worker[0].specialization, description=worker[0].description,location_id=worker[0].location_id)
                await self.check_two_workers_time(worker=worker,schedule=schedule)
            new_schedule = Schedule(worker_id=schedule.worker_id,date=schedule.date, start_time=schedule.start_time, end_time=schedule.end_time)
            self.session.add(new_schedule)
            await self.session.commit()
            return Schedule(id=new_schedule.id,worker_id=schedule.worker_id, date=schedule.date, start_time=schedule.start_time, end_time=schedule.end_time)


    async def get_schedules(self, page: int) -> list[ScheduleSchema]:
        params = Params(page=page, size=10)
        schedules = await paginate(self.session, select(Schedule), params=params)
        return [ScheduleSchema(id=schedule.id, worker_id=schedule.worker_id,date=schedule.date, start_time=schedule.start_time, end_time=schedule.end_time) for schedule in schedules.items]


    async def delete_schedule(self, schedule_id):
        schedule_tobe_deleted = await self.session.get(Schedule,schedule_id)
        if schedule_tobe_deleted:
            await self.session.delete(schedule_tobe_deleted)
            await self.session.commit()
            return HTTPException(200,detail=f"Schedule with id {schedule_tobe_deleted.id} is successfully deleted")
    

    async def get_schedule_for_worker(self, worker_id: int ) -> list[ScheduleSchema]:
        schedules = await self.session.execute(select(Schedule).filter(Schedule.worker_id == worker_id))
        return [ScheduleSchema(id=schedule[0].id, worker_id=schedule[0].worker_id, date=schedule[0].date, start_time=schedule[0].start_time, end_time=schedule[0].end_time) for schedule in schedules]


    async def check_worker_schedule(self,schedule: Union[ScheduleCreateSchema,ScheduleAlterSchema]) -> bool:
        ## if a worker has 9: 00 - 12:00 and an admin wants to add  13:00 - 17:00 ,it should pass
        ## Checking for the identical dates 
        db_schedule = await self.session.execute(select(Schedule).filter(and_(
            Schedule.worker_id == schedule.worker_id,
            Schedule.date == schedule.date,
            Schedule.start_time == schedule.start_time,
            Schedule.end_time == schedule.end_time)))
        db_schedule = db_schedule.scalars().first()
        if db_schedule:
            raise HTTPException(403,f"Worker has the same schedule of  start_time,end_time and date!")
        ## checking for working hours inside working hours
        list_schedules = await self.session.execute(select(Schedule).filter(Schedule.worker_id == schedule.worker_id))
        for new_schedule in list_schedules:
            if new_schedule[0].date == schedule.date and new_schedule[0].end_time > schedule.start_time and schedule.start_time > new_schedule[0].start_time:
                raise HTTPException(403,"Worker is already working in these times!")
        return True
                        ## if a worker has 9: 00 - 12:00 and an admin wants to add  11:00 - 17:00 ,it should fail
        
        ## old_end_time(12:00) > new.start_time(11:00) > old.start_time(9:00) -> fail 
        ## 12:00 < 13:00 -> pass

    async def check_two_workers_time(self,worker,schedule) -> bool:
        db_workers = await self.session.execute(select(Worker).filter(and_(Worker.specialization == worker.specialization, Worker.location_id == worker.location_id)))
        for db_worker in db_workers:
            db_worker_schedules = await self.session.execute(select(Schedule).filter(Schedule.worker_id == db_worker[0].id))
            new_worker_schedule = schedule
            for db_worker_schedule in db_worker_schedules:
                if new_worker_schedule.date == db_worker_schedule[0].date and new_worker_schedule.end_time >= db_worker_schedule[0].start_time and db_worker_schedule[0].end_time >= new_worker_schedule.start_time:
                    raise HTTPException(403,"Two workers with the same specialization cannot work in one location at the same time !")
                if  new_worker_schedule.date == db_worker_schedule[0].date and new_worker_schedule.start_time == db_worker_schedule[0].start_time and new_worker_schedule.end_time == db_worker_schedule[0].end_time:
                    raise HTTPException(403,"Two workers with the same specialization cannot work in one location at the same time!")
        return True   
        




async def get_schedule(id: int, session: AsyncSession = Depends(get_session), user: User = Depends(get_user)) -> Schedule:
    if user.admin:
        schedule = await session.get(Schedule, id)
        if schedule:
                return schedule
        else:
            raise HTTPException(404, 'Schedule not found')
    raise HTTPException(404,"You are not authorized for this action!")