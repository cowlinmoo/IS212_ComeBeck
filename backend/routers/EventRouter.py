from typing import List, Annotated
from fastapi import APIRouter, Depends

from backend.models.enums.EmployeeRoleEnum import EmployeeRole
from backend.schemas.EventSchema import EventSchema
from backend.services.EventService import EventService
from backend.services.dependencies import role_required

EventRouter = APIRouter(
    prefix="/api/event",
    tags=["Event Endpoints"],
)

@EventRouter.get("", response_model=List[EventSchema])
def get_all_events(event_service: EventService = Depends(),
                    current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))):
    return event_service.get_all_events()

@EventRouter.get("/{event_id}", response_model=EventSchema)
def get_event_by_event_id(event_id: int, event_service: EventService = Depends(),
                          current_user: dict = Depends(role_required(EmployeeRole.HR, EmployeeRole.MANAGER, EmployeeRole.STAFF))):
    return event_service.get_event_by_event_id(event_id)