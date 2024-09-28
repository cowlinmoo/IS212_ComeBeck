from fastapi import HTTPException
from typing import List, Type

from fastapi import Depends
from sqlalchemy.orm import Session

from ..config.Database import get_db_connection
from backend.models import Event

class EventRepository:
    db: Session

    def __init__(self, db: Session = Depends(get_db_connection)):
        self.db = db

    def get_all_events(self) -> List[Type[Event]]:
        events = self.db.query(Event).all()
        return events if events is not None else []

    def get_event_by_event_id(self, event_id: int) -> Event:
        event = self.db.query(Event).filter(Event.event_id == event_id).first()
        if event is not None:
            return event
        else:
            raise HTTPException(status_code=404, detail="Event not found")

    def get_event_by_application_id(self, application_id: int) -> List[Type[Event]]:
        events = self.db.query(Event).filter(Event.application_id == application_id).all()
        return events if events is not None else []

    def create_event(self, event: Event) -> Event:
        self.db.add(event)
        self.db.commit()
        self.db.refresh(event)
        return event

    def update_event(self, event_id: int, event: Event) -> Event:
        event_to_update = self.get_event_by_event_id(event_id)
        for key, value in event.items():
            setattr(event_to_update, key, value)
        self.db.commit()
        self.db.refresh(event_to_update)
        return event_to_update

    def delete_event(self, event_id: int) -> Event:
        event_to_delete = self.get_event_by_event_id(event_id)
        self.db.delete(event_to_delete)
        self.db.commit()
        return event_to_delete
    
    def get_events_by_application_ids(self, application_ids: List[int]) -> List[Type[Event]]:
        return self.db.query(Event).filter(Event.application_id.in_(application_ids)).all()
