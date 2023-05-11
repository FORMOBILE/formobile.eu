"""
Module to get all available Calendars of a specified google calendar user
"""
import logging

from google_calendar.cal_setup import get_calendar_service


def list_calendars(token: str) -> list:
    """
    Lists all available Calendars

    :param token: path to token of the google user
    :return: list of event dicts
    """
    service = get_calendar_service(token)
    # Call the Calendar API
    logging.info('Getting list of calendars')
    calendars_result = service.calendarList().list().execute()

    calendars = calendars_result.get('items', [])

    if not calendars:
        logging.info('No calendars found.')
    for calendar in calendars:
        summary = calendar['summary']
        calendar_id = calendar['id']
        primary = "Primary" if calendar.get('primary') else ""
        logging.info(f"{summary}\t{calendar_id}\t{primary}")
    return calendars
