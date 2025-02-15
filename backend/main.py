from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.config.Database import init_db
from backend.models.BaseModel import create_database
from backend.routers.DepartmentRouter import DepartmentRouter
from backend.routers.EventRouter import EventRouter
from backend.routers.ApplicationRouter import ApplicationRouter
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter
from backend.routers.TeamRouter import TeamRouter
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
app.include_router(DepartmentRouter)
app.include_router(TeamRouter)
