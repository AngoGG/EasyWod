from datetime import datetime, date, timedelta
from event.models import Event


def get_all_week_events():
    '''This method calculates the start and end dates 
    of the current week
    then get all the week's events and reports it.
    '''

    today = date.today()
    day = today.weekday()

    interval_start = 0 - day
    interval_end = 6 - day

    date_start_week = today + timedelta(days=interval_start)
    date_end_week = today + timedelta(days=interval_end)

    week_events = Event.objects.filter(
        start__range=[date_start_week, date_end_week]
    ).count()

    return week_events

