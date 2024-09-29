from typing import List

from fastapi import Depends

from backend.models import Event
from backend.repositories.EventRepository import EventRepository

class EventService:
    eventRepository: EventRepository

    def __init__(
        self, eventRepository: EventRepository = Depends()
    ) -> None:
        self.eventRepository = eventRepository

    def get_all_events(self):
        return self.eventRepository.get_all_events()

    def get_event_by_event_id(self, event_id: int):
        return self.eventRepository.get_event_by_event_id(event_id)

    def get_event_by_application_id(self, application_id: int):
        return self.eventRepository.get_event_by_application_id(application_id)

    def create_event(self, event) -> Event:
        return self.eventRepository.create_event(event)

    def update_event(self, event_id, event):
        return self.eventRepository.update_event(event_id, event)

    def delete_event(self, event_id):
        return self.eventRepository.delete_event(event_id)

    def create_multiple_events(self, events: List[Event]) -> List[Event]:
        created_events = []
        for event in events:
            created_event = self.eventRepository.create_event(event)
            created_events.append(created_event)
        return created_events