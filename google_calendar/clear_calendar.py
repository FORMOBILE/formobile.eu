"""
Module to clear an existing google calendar
"""
import logging
import os.path

from google_calendar.cal_setup import get_calendar_service


def clear_calendar(token: str, calendar_id='primary') -> None:
    """
    Clears the primary calendar of the google calendar by default.

    :param token: path to token of user
    :param calendar_id: id of calendar, primary by default
                        - can be changed to clear non primary calendars e.g. shared calendars
    :return: Nothing
    """
    service = get_calendar_service(token)
    service.calendars().clear(calendarId=calendar_id).execute()
    logging.info(f'Cleared {calendar_id} from {os.path.basename(token)}')
