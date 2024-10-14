from fastapi import HTTPException
from typing import List, Type

from fastapi import Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from backend.config.Database import get_db_connection
from backend.models import Application
from backend.models.generators import get_current_datetime_sgt
from backend.schemas.ApplicationSchema import ApplicationWithdrawSchema, \
    ApplicationCreateSchema


class ApplicationRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_applications(self) -> List[Type[Application]]:
        applications = self.db.query(Application).all()
        return applications if applications is not None else []

    def get_application_by_application_id(self, application_id: int) -> Application:
        application = self.db.query(Application).filter(
            Application.application_id == application_id).first()
        if application is not None:
            return application
        else:
            raise HTTPException(
                status_code=404, detail="Application not found")

    def get_application_by_staff_id(self, staff_id: int) -> List[Type[Application]]:
        applications = self.db.query(Application).filter(
            Application.staff_id == staff_id).all()
        return applications if applications is not None else []

    def create_application(self, application: dict) -> Application:
        new_application = Application(**application)
        self.db.add(new_application)
        self.db.commit()
        self.db.refresh(new_application)
        return new_application

    def withdraw_application(self, application_id: int, application: ApplicationWithdrawSchema) -> Application:
        db_application = self.get_application_by_application_id(application_id)

        db_application.status = application.status
        db_application.outcome_reason = application.withdraw_reason
        db_application.last_updated_on = get_current_datetime_sgt()

        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def update_application(self, application_id: int, application: ApplicationCreateSchema) -> Application:
        db_application = self.db.query(Application).filter(
            Application.application_id == application_id).first()
        if db_application is None:
            raise HTTPException(
                status_code=404, detail="Application not found")

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

    def update_application_status(self, application_id: int, new_status: str, outcome_reason: str) -> Application:
        db_application = self.db.query(Application).filter(Application.application_id == application_id).first()
        if db_application is None:
            raise HTTPException(
                status_code=404, detail="Application not found")

        db_application.status = new_status
        db_application.outcome_reason = outcome_reason
        db_application.last_updated_on = get_current_datetime_sgt()

        self.db.commit()
        self.db.refresh(db_application)
        return db_application

    def get_pending_applications(self) -> List[Type[Application]]:
        return self.db.query(Application).filter(Application.status == 'pending').all()

    def get_applications_by_approver_id(self, approver_id):
        return self.db.query(Application).filter(Application.approver_id == approver_id).all()

    def get_application_status_by_application_id(self, application_id: int) -> str:
        application = self.get_application_by_application_id(application_id)
        return application.status

    def update_application_state(self, application_id, new_state, outcome_reason, status):
        db_application = self.get_application_by_application_id(application_id)
        db_application.application_state = new_state
        db_application.status = status
        db_application.outcome_reason = outcome_reason
        self.db.commit()
        self.db.refresh(db_application)
        return db_application
