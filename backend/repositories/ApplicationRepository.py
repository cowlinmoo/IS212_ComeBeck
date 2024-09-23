from fastapi import HTTPException
from typing import List, Type

from fastapi import Depends
from passlib.context import CryptContext
from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..config.Database import get_db_connection
from ..models import Application
from ..models.generators import get_current_datetime_sgt
from ..schemas.ApplicationSchema import ApplicationCreateSchema, ApplicationUpdateSchema

class ApplicationRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_applications(self) -> List[Type[Application]]:
        applications = self.db.query(Application).all()
        return applications if applications is not None else []

    def get_application_by_application_id(self, application_id: int) -> Application:
        application = self.db.query(Application).filter(Application.application_id == application_id).first()
        if application is not None:
            return application
        else:
            raise HTTPException(status_code=404, detail="Application not found")

    def get_application_by_staff_id(self, staff_id: int) -> List[Type[Application]]:
        applications = self.db.query(Application).filter(Application.staff_id == staff_id).all()
        return applications if applications is not None else []

    def create_application(self, application: dict) -> Application:
        new_application = Application(**application)
        self.db.add(new_application)
        self.db.commit()
        self.db.refresh(new_application)
        return new_application

    def update_application(self, application_id: int, application: ApplicationUpdateSchema) -> Application:
        db_application = self.db.query(Application).filter(Application.application_id == application_id).first()
        if db_application is None:
            raise HTTPException(status_code=404, detail="Application not found")

        update_data = application.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_application, key, value)

        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def get_applications_by_status(self, status: str) -> List[Type[Application]]:
        applications = self.db.query(Application).filter(Application.status == status) \
            .order_by(desc(Application.created_on))
        return applications if applications is not None else []

    def update_application_status(self, application_id: int, new_status: str) -> Application:
        db_application = self.db.query(Application).filter(Application.application_id == application_id).first()
        if db_application is None:
            raise HTTPException(status_code=404, detail="Application not found")

        db_application.status = new_status
        db_application.last_updated_on = get_current_datetime_sgt()

        self.db.commit()
        self.db.refresh(db_application)
        return db_application