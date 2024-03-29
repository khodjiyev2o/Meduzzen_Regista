from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from app.routers import users, locations, workers, procedures, schedules, appointments, for_users




def configure(app):
    origins = [
        "http://localhost",
        "http://localhost:8000",
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    add_pagination(app)

    app.include_router(workers.worker_router)
    app.include_router(users.user_router)
    app.include_router(appointments.appointment_router)
    app.include_router(locations.location_router)
    app.include_router(procedures.procedure_router)
    app.include_router(schedules.schedule_router)
    app.include_router(for_users.for_users_router)