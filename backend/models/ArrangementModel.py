from sqlalchemy import Column, BigInteger, Text, Boolean, ForeignKey
from backend.models.BaseModel import EntityMeta


class Arrangement(EntityMeta):
    __tablename__ = 'arrangement'

    arrangement_id = Column(BigInteger, primary_key=True)
    reason = Column(Text, nullable=False)
    description = Column(Text, nullable=False)
    recurring = Column(Boolean, nullable=False)
    application_id = Column(BigInteger, ForeignKey(
        'application.application_id'), nullable=False)

    class Config:
        orm_mode = True
