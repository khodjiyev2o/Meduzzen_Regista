from app.schemas.users import UserCreateSchema, UserSchema, UserLoginSchema, UserAlterSchema
from app.schemas.workers import WorkerCreateSchema,WorkerSchema
from app.schemas.locations import LocationCreateSchema,LocationSchema
from app.schemas.procedures import ProcedureSchema, ProcedureCreateSchema
from app.schemas.schedules import ScheduleSchema, ScheduleCreateSchema
from app.schemas.appointments import AppointmentSchema, AppointmentCreateSchema


user1 = UserCreateSchema(username='user1', email='mail1@mail.com',  description='first', password1='password1', password2='password1',admin=True)
user2 = UserCreateSchema(username='user2', email='mail2@mail.com',  description='second', password1='password2', password2='password2')
user3 = UserCreateSchema(username='user3', email='mail3@mail.com',  description='third', password1='password3', password2='password3')


db_user1 = UserSchema(id=1, username='user1', email='mail1@mail.com', description='first')
db_user2 = UserSchema(id=2, username='user2', email='mail2@mail.com', description='second')
db_user3 = UserSchema(id=3, username='user3', email='mail3@mail.com', description='third')



login_user1 = UserLoginSchema(email='mail1@mail.com', password='password1')
login_user2 = UserLoginSchema(email='mail2@mail.com', password='password2')

## locations 
location1 = LocationCreateSchema(placename="Daejeon",latitude=123,longitude=123)
location2 = LocationCreateSchema(placename="Seoul",latitude=123,longitude=123)

db_location1 = LocationSchema(id=1,placename="Daejeon",latitude=123,longitude=123)
db_location2 = LocationSchema(id=2,placename="Seoul",latitude=123,longitude=123)

worker1 = WorkerCreateSchema(user_id=2, specialization="doctor", description="good doctor",location_id=1)
worker2 = WorkerCreateSchema(user_id=3,specialization="doctor", description="good doctor",location_id=1)
db_worker1 = WorkerSchema(id=1,user_id=2, specialization="doctor", description="good doctor",location_id=1)
db_worker2 = WorkerSchema(id=2,user_id=3, specialization="doctor", description="good doctor",location_id=1)



procedure1 = ProcedureCreateSchema(name='fizioterapiya',worker_id=1,duration=1,description='Awesome procedure done by an expert')
procedure2 = ProcedureCreateSchema(name='massage',worker_id=2,duration=2,description='Awesome procedure done by an expert')


db_procedure1 = ProcedureSchema(id=1,name='fizioterapiya',worker_id=1,duration=1,description='Awesome procedure done by an expert')
db_procedure2 = ProcedureSchema(id=2,name='massage',worker_id=2,duration=2,description='Awesome procedure done by an expert')

schedule1 = ScheduleCreateSchema(worker_id=1,date="2022-11-26",start_time="9:00",end_time="17:00")
schedule2 = ScheduleCreateSchema(worker_id=2,date="2022-11-26",start_time="9:00",end_time="17:00")

db_schedule1 = ScheduleSchema(id=1,worker_id=1,date="2022-11-26",start_time="9:00",end_time="17:00")
db_schedule2 = ScheduleSchema(id=2,worker_id=2,date="2022-11-26",start_time="9:00",end_time="17:00")


