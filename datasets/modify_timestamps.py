"""
Module with functions to change the timestamps of files
"""
import logging
import os
import time
from datetime import datetime, timedelta
import random


def random_date(start: datetime, end: datetime) -> datetime:
    """
    Generate a random datetime between `start` and `end`
    :param start: start time
    :param end: end time
    :return: random datetime
    """
    start = datetime.strptime(str(start), "%Y-%m-%d %H:%M:%S.%f")
    end = datetime.strptime(str(end), "%Y-%m-%d %H:%M:%S.%f")
    start_seconds = time.mktime(start.timetuple())
    end_seconds = time.mktime(end.timetuple())
    return start + timedelta(
        # Get a random amount of seconds between `start` and `end`
        seconds=random.randint(0, int(end_seconds - start_seconds))
    )


def modify_timestamps(directory: str, start: datetime, end: datetime) -> None:
    """
    Modifies all files in the given directory with random dates between start date and end date.

    :param directory: directory
    :param start: start date
    :param end: end date
    :return: Nothing
    """
    for file in os.listdir(directory):
        filepath = os.path.join(directory, file)
        date = random_date(start, end)
        mod_time = time.mktime(date.timetuple())
        os.utime(filepath, (mod_time, mod_time))
        logging.info(f'Modified {filepath} with {mod_time}')
