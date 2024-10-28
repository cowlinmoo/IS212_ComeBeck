from datetime import timedelta
from typing import List

from fastapi import Depends

from backend.models import Event
from backend.models.enums.RecurrenceType import RecurrenceType
from backend.repositories.EventRepository import EventRepository
from backend.schemas.ApplicationSchema import ApplicationCreateSchema


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

    def create_events(self, application: ApplicationCreateSchema, application_id: int):
        if application.events:
            for event in application.events:
                new_event = Event(
                    requested_date=event.requested_date,
                    location=application.location,
                    application_id=application_id,
                    application_hour=event.application_hour
                )
                self.create_event(new_event)
        elif application.recurring:
            self.create_recurring_events(application, application_id)
        else:
            self.create_single_event(application, application_id)

    def create_single_event(self, application: ApplicationCreateSchema,
                            application_id: int):
        event = Event(
            requested_date=application.requested_date,
            location=application.location,
            application_id=application_id,
            application_hour=application.application_hour
        )
        self.create_event(event)

    def create_recurring_events(self, application: ApplicationCreateSchema,
                                application_id: int):
        current_date = application.requested_date
        end_date = application.end_date or (
            current_date + timedelta(days=365))
        # Default to one year if no end_date

        while current_date <= end_date:
            event = Event(
                requested_date=current_date,
                location=application.location,
                application_id=application_id,
                application_hour=application.application_hour
            )
            self.create_event(event)

            if application.recurrence_type == RecurrenceType.DAILY:
                current_date += timedelta(days=1)
            elif application.recurrence_type == RecurrenceType.WEEKLY:
                current_date += timedelta(weeks=1)
            elif application.recurrence_type == RecurrenceType.MONTHLY:
                # Move to the same day next month
                if current_date.month == 12:
                    current_date = current_date.replace(year=current_date.year + 1,
                                                        month=1)
                else:
                    current_date = current_date.replace(month=current_date.month + 1)
