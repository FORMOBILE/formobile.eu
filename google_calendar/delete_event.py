"""
Module to delete a specific event from a google calendar
"""
import logging
import os.path

import googleapiclient

from cal_setup import get_calendar_service


def delete_event(token: str, event_id: str, calendar_id='primary') -> None:
    """
    Deletes a specified event from the google calendar
    :param token: token of the user whose event is to be updated
    :param event_id: id of the event that should be deleted
    :param calendar_id: set to primary by default
                        - can be changed to delete events of non primary calendars e.g. shared calendars
    :return: Nothing
    """

    service = get_calendar_service(token)
    try:
        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id,
        ).execute()
        logging.info(f'Deleted {event_id} for {os.path.basename(token)} in {calendar_id} calendar')
    except googleapiclient.errors.HttpError:
        logging.warning(f"Failed to delete {event_id} for {os.path.basename(token)} in {calendar_id} calendar")
