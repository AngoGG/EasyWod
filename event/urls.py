from django.urls import include, path
from .views import EventView

app_name: str = "event"

urlpatterns = [
    path(r"", EventView.as_view(), name="event_calendar"),
]
