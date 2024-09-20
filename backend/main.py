from fastapi import FastAPI

from backend.models.BaseModel import create_database
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter

create_database()
app = FastAPI(
    title="ComeBeck Backend API",  # Add a descriptive title
    description="This is the backend for ComeBeck and it is built using FastAPI",
    version="1.0.0",
    docs_url="/api/documentation",
)

app.include_router(AuthRouter)
app.include_router(EmployeeRouter)


