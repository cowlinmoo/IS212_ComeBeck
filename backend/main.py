from fastapi import FastAPI

from backend.config.Database import init_db
from backend.models.BaseModel import create_database
from backend.routers.ApplicationRouter import ApplicationRouter
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter

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



