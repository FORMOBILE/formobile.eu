"""
Module to create a new event in google calendar
"""
import logging
import os.path

from google_calendar.google_calendar.cal_setup import get_calendar_service


def create_event(token: str, event_data: str, notifications=False, calendar_id='primary') -> dict:
    """
    Creates an google calendar event

    :param calendar_id: set to primary by default
                        - can be changed to create events of non primary calendars e.g. shared calendars
    :param notifications: option to send notifications to all members of the event
    :param token: path to token of the calendar owner
    :param event_data: data of the event to be created - more info in write_events.py
    :return: data of the created event as dict
    """
    service = get_calendar_service(token)

    event_result = service.events().insert(calendarId=calendar_id, sendNotifications=notifications,
                                           body=event_data).execute()
    log_string = f'Created event: {event_data} for {os.path.basename(token)} in {calendar_id} calendar'
    if notifications:
        log_string += ' and send notifications to participants'
    logging.info(log_string)

    return event_result
