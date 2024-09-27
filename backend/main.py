from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

from backend.config.Database import init_db , get_db_connection
from backend.models.BaseModel import create_database
from backend.routers.EventRouter import EventRouter
from backend.routers.ApplicationRouter import ApplicationRouter
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter
from backend.repositories.ApplicationRepository import ApplicationRepository
from backend.services.ApplicationService import ApplicationService
from backend.repositories.EmployeeRepository import EmployeeRepository
from backend.services.EmailService import EmailService
from backend.repositories.EventRepository import EventRepository
from backend.services.EventService import EventService

create_database()
init_db()
app = FastAPI(
    title="ComeBeck Backend API",  # Add a descriptive title
    description="This is the backend for ComeBeck and it is built using FastAPI",
    version="1.0.0",
    docs_url="/api/documentation",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(AuthRouter)
app.include_router(ApplicationRouter)
app.include_router(EmployeeRouter)
app.include_router(EventRouter)


scheduler = BackgroundScheduler()
db = next(get_db_connection())
application_repository = ApplicationRepository(db)
employee_repository = EmployeeRepository(db)
event_repository = EventRepository(db)
email_service = EmailService()
event_service = EventService()
application_service = ApplicationService(application_repository, employee_repository, email_service,event_repository, event_service)

@app.on_event("startup")
async def start_scheduler():
    scheduler.add_job(
        application_service.reject_old_applications,
        trigger=CronTrigger(minute='*'),  # Run at midnight
        id="reject_old_applications",
        name="Reject applications with events older than two months",
        replace_existing=True,
    )
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_scheduler():
    scheduler.shutdown()


