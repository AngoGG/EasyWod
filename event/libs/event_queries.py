from datetime import datetime, date, timedelta
from event.models import Event, EventMember


def get_all_week_events():
    '''This method calculates the start and end dates 
    of the current week
    then get all the week's events and reports it.
    '''

    today = date.today()
    day = today.weekday()

    interval_start = 0 - day
    interval_end = 6 - day

    query_date_start_week = today + timedelta(days=interval_start)
    query_date_end_week = today + timedelta(days=interval_end + 1)

    week_events = Event.objects.filter(
        start__gte=query_date_start_week, start__lte=query_date_end_week,
    )

    return week_events


def get_weeks_events_average_attendees():
    # Get week events
    # Get all the events members
    # Divide events members by events and return the average
    week_events = get_all_week_events()
    total_members = 0

    for event in week_events:
        total_members += event.reserved_slot

    return total_members / week_events.count()

