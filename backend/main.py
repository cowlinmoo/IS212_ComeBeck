from fastapi import FastAPI
from apscheduler.schedulers.background import BackgroundScheduler

from backend.config.Database import init_db
from backend.models.BaseModel import create_database
from backend.routers.EventRouter import EventRouter
from backend.routers.ApplicationRouter import ApplicationRouter
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter
from backend.services.ApplicationService import ApplicationService, setup_application_cleanup_scheduler


create_database()
init_db()
app = FastAPI(
    title="ComeBeck Backend API",  # Add a descriptive title
    description="This is the backend for ComeBeck and it is built using FastAPI",
    version="1.0.0",
    docs_url="/api/documentation",
)

app.include_router(AuthRouter)
app.include_router(ApplicationRouter)
app.include_router(EmployeeRouter)
app.include_router(EventRouter)


application_service = ApplicationService()

scheduler = setup_application_cleanup_scheduler(application_service)

@app.on_event("startup")
async def startup_event():
    scheduler.start()

@app.on_event("shutdown")
async def shutdown_event():
    scheduler.shutdown()


