"""
Module to determine spare time
"""
import datetime


def is_enjoying(person):
    """
    Checks if a person is currently active, based on the times given in the config file.

    Assumptions:
                        - the keys of active times in the config file needs to be formatted like H:MM or HH:MM (e.g.
                          6:10 or 12:00)
                        - the values of the keys are integers and are defined as minutes

    :param person: the persons defined in the config file, e. g. config['People'][0]
    :return: True/False if person is currently active
    """

    started = person['Mobile devices'][0]['spare time']
    for start_key in started:
        # Hour of start being active
        start_hour = int(start_key.partition(":")[0])
        # Minute of start being active
        start_minute = int(start_key.partition(":")[2])
        # Duration of being active
        active_time = started[start_key]

        # Start time
        start = str(datetime.time(start_hour, start_minute))

        # Calculating the end time
        starting = datetime.datetime(2021, 1, 1, start_hour, start_minute, 00)
        ending = str(starting + datetime.timedelta(minutes=active_time))

        # Formatting
        ended = ending.partition(" ")[2]
        # Hour of end being active
        end_hour = int(ended.partition(":")[0])
        # Minute of end being active
        ending_minute = ended.partition(":")[2]
        end_minute = int(ending_minute.partition(":")[0])

        # End time
        end = str(datetime.time(end_hour, end_minute))
        # Current time on the operating system clock
        now = datetime.datetime.now()
        current_time = now.strftime('%H:%M:%S')

        if start < current_time < end:
            return True
        if end < start < current_time:
            return True
        if current_time < end < start:
            return True

    return False
