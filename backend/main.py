from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI

from backend.models.BaseModel import create_database
from backend.routers.AuthenticationRouter import AuthRouter
from backend.routers.EmployeeRouter import EmployeeRouter

create_database()
app = FastAPI()

app.include_router(EmployeeRouter)
app.include_router(AuthRouter)

