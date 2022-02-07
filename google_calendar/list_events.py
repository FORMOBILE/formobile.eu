"""
Module to view the next n upcoming events of a google calendar
"""
import datetime
import logging

from cal_setup import get_calendar_service


def list_events(token: str, number_of_events: int, calendar_id='primary') -> list:
    """
    Lists the next n events of the calendar
    :param token: token of the calendar owner
    :param number_of_events: number of events to be returned
    :param calendar_id: set to primary by default
                        - can be changed to delete events of non primary calendars e.g. shared calendars
    :return: list of event dicts
    """
    service = get_calendar_service(token)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    logging.info(f'Getting List of up to {number_of_events} events')
    events_result = service.events().list(
        calendarId=calendar_id, timeMin=now,
        maxResults=number_of_events, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        logging.info('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        logging.info(start, event['summary'], event['id'])
    return events
