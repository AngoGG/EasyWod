from django.urls import include, path
from .views import AddEvent, CalendarView

app_name: str = "event"

urlpatterns = [
    path(r"", CalendarView.as_view(), name="event_calendar"),
    path("add_event", AddEvent.as_view(), name="add_event"),
]
