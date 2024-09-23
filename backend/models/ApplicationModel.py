from sqlalchemy import CheckConstraint, Column, BigInteger, ForeignKey, Text, DateTime, String
from backend.models.BaseModel import EntityMeta
from backend.models.generators import get_current_datetime_sgt


class Application(EntityMeta):
    __tablename__ = 'application'

    application_id = Column(BigInteger, primary_key=True)
    reason = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
    created_on = Column(DateTime, nullable=False,
                        default=get_current_datetime_sgt)
    last_updated_on = Column(DateTime, nullable=True,
                             default=get_current_datetime_sgt)
    status = Column(String(20), CheckConstraint(
        "status IN ('approved', 'pending', 'rejected', 'withdrawn')"), nullable=False)
    staff_id = Column(ForeignKey('employees.staff_id'), nullable=False)
    approver_id = Column(ForeignKey('employees.staff_id'), nullable=True)

    class Config:
        orm_mode = True
