import uuid
from src.models.repository.attendees_repository import AttendeesRepository
from src.http_types.http_request import HttpRequest
from src.http_types.http_response import HttpResponse
from src.models.repository.events_repository import EventsRepository

class AttendeesHandler:
    def __init__(self) -> None:
        self.__atendees_repository = AttendeesRepository()
        self.__events_repository = EventsRepository()

    def registry(self, http_request: HttpRequest) -> HttpResponse:
        body = http_request.body
        event_id = http_request.param["event_id"]

        event_attendees_count = self.__events_repository.count_event_attendees(event_id)
        if(
            event_attendees_count["attendeesAmount"]
            and event_attendees_count["maximumAttendees"] < event_attendees_count["attendeesAmount"]
        ): raise Exception("Evento Lotado")

        body["uuid"] = str(uuid.uuid4())
        body["event_id"] = event_id
        self.__atendees_repository.insert_attendee(body)

        return HttpResponse(body = None, status_code = 201)

    def find_attendee_badge(self, http_request: HttpRequest) -> HttpResponse:
        attendee_id = http_request.param["attendeeId"]
        badge = self.__atendees_repository.get_attendee_badge_by_id(attendee_id)
        if not badge: raise Exception("Participante não encontrado")

        return HttpResponse(
            body={
                "badge": {
                    "name": badge.name,
                    "email": badge.email, 
                    "eventTitle": badge.title
                }
            },
            status_code= 200
        )

    def find_attendees_from_event(self, http_request: HttpRequest) -> HttpResponse:
        event_id = http_request.param["event_id"]
        attendees = self.__atendees_repository.get_attendee_badge_by_id(event_id)
        if not attendees: raise Exception("Participantes não encontrados")

        formatted_attendees = []
        for atteendee in attendees:
            formatted_attendees.append(
                {
                    "id": attendee.id,
                    "name": atteendee.name,
                    "email": atteendee.email,
                    "checkedInAt": atteendee.checkedInAt,
                    "createdAt": attendee.createdAt
                }
            )

        return HttpResponse(
            body = {"attendees": formatted_attendees},
            status_code = 200
        )