"""
This module updates a google calendar event
"""
import logging
import os.path

from cal_setup import get_calendar_service
from googleapiclient.errors import HttpError


def update_event(token: str, event_id: str, updated_event_data: str, calendar_id='primary') -> dict or bool:
    """
    Updates an existing google calendar event
    :param token: token of the user whose event is to be updated
    :param event_id: id of the event that should be updated
    :param updated_event_data: updated data of the event - must contain at least start-and end times
    :param calendar_id: set to primary by default
                        - can be changed to change events of non primary calendars e.g. shared calendars
    :return: data of the updated event as a dict
    """
    try:
        service = get_calendar_service(token)
        event_result = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=updated_event_data,
        ).execute()
        logging.info(f'Updated event {event_id} for {token} in {calendar_id} calendar')
    except HttpError:
        logging.warning(f'Failed to update event {event_id} for {os.path.basename(token)} in {calendar_id} calendar')
        return False

    return event_result
