from sqlalchemy import (CheckConstraint, Column, BigInteger, ForeignKey, Text, DateTime,
                        String, Boolean, Date, Enum as SQLAlchemyEnum)
from sqlalchemy.orm import relationship

from backend.models.BaseModel import EntityMeta
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.models.generators import get_current_datetime_sgt


class Application(EntityMeta):
    __tablename__ = 'application'

    application_id = Column(BigInteger, primary_key=True)
    reason = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_on = Column(DateTime, nullable=False, default=get_current_datetime_sgt)
    last_updated_on = Column(DateTime, nullable=True, default=get_current_datetime_sgt)
    status = Column(String(20),
                    CheckConstraint("status IN ('approved', 'pending',"
                                    "'rejected', 'withdrawn', 'superseded')"),
                    nullable=False)
    application_state = Column(Text,
                               CheckConstraint("application_state IN "
                                               "('new_application',"
                                               "'cancel_one_request', 'cancel_request',"
                                               "'change_request')"), nullable=True)
    staff_id = Column(ForeignKey('employees.staff_id'), nullable=False)
    approver_id = Column(ForeignKey('employees.staff_id'), nullable=True)
    outcome_reason = Column(Text, nullable=True)
    original_application_id = Column(BigInteger,
                                     ForeignKey('application.application_id'),
                                     nullable=True)

    # fields for recurring events
    recurring = Column(Boolean, nullable=False)
    recurrence_type = Column(SQLAlchemyEnum(RecurrenceType), nullable=True)
    end_date = Column(Date, nullable=True)

    # Relationships
    events = relationship("Event", back_populates="application")
    staff = relationship("Employee", foreign_keys="Application.staff_id",
                         back_populates="applications")
    approver = relationship("Employee", foreign_keys="Application.approver_id",
                            back_populates="approved_applications")
    original_application = relationship("Application",
                                        remote_side="Application.application_id",
                                        backref="change_requests")
