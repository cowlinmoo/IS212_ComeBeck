from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.models.BaseModel import create_database
from backend.routers.EmployeeRouter import EmployeeRouter

create_database()
app = FastAPI()

app.include_router(EmployeeRouter)

