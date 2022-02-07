"""
Main module for calendar.
"""
import logging
import os
import json

from definitions import CONFIG_PATH, ROOT_DIR
from google_calendar.google_calendar import write_events
from google_calendar.google_calendar.clear_calendar import clear_calendar
from google_calendar.google_calendar.create_event import create_event


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
)


with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)


def populate_calendar(delete: bool) -> None:
    """
    Main function to populate all Google Calendars of the people listed in the config file.
    :param delete: whether the existing entries in the calendar should be deleted
    :return: Nothing
    """
    for person in config['People']:
        token_dir = os.path.join(ROOT_DIR, 'Token',
                                 person['Mobile devices'][0]['Whatsapp token'],
                                 person['Gmail account'][0]['Calendar token'])
        events = os.path.join(ROOT_DIR, 'google_calendar', 'events',
                              f"{person['Mobile devices'][0]['Whatsapp token']}.csv")

        if delete:
            clear_calendar(token_dir)
        if os.path.exists(events):
            event_dict = write_events.write_event(events)
            for eve in event_dict:
                logging.info(f'Creating event {eve}')
                create_event(token_dir, eve)


populate_calendar(True)
