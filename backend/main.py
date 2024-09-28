from contextlib import asynccontextmanager

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
from backend.services.dependencies import get_scheduler_service

create_database()
init_db()
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    scheduler_service = get_scheduler_service()
    scheduler_service.start()
    yield
    # Shutdown
    scheduler_service.stop()
app = FastAPI(
    title="ComeBeck Backend API",  # Add a descriptive title
    description="This is the backend for ComeBeck and it is built using FastAPI",
    version="1.0.0",
    docs_url="/api/documentation",
    lifespan=lifespan
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
