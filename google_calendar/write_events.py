"""
Module to get Google Calendar Event from csv
"""
import pandas as pd


def write_event(filepath: str) -> list:
    """
    Reads the csv and converts the data to a google calendar event

    An event needs to have at least a start and end time and a timezone.

    Assumptions:
        - The columns of the .csv are exactly: description, location, start, end, timezone, organizer, attendees,
        recurrence, how often, specify days
            -> not necessarily in this order
        - timezone: Formatted as an IANA Time Zone Database name, e.g. "Europe/Zurich" (Google Calendar API Reverence)
        - times (start, end): formatted in 'ISO 8601': YYYY-MM-DDTHH:MM:SS
        - description: string
        - location: string
        - organizer: email address of the calendar owner (= the one the token belongs to)
        - attendees: email addresses of attendees, separated by newline
        - recurrence: can only be: daily, weekly, monthly, yearly
        - how often: how often the event should be repeated
        - specific days: days where the event should be repeated, separated by comma e.g. "FR,MO,TU"

    :param filepath: path to the .csv file
    :return: Google Calendar events in form of a list of dicts
    """
    # read csv
    data_frame = pd.read_csv(filepath)
    data_frame = data_frame.fillna(" ")

    # drop rows that have no start, end or timezone
    data_frame = data_frame[data_frame.timezone != " "]
    data_frame = data_frame[data_frame.start != " "]
    data_frame = data_frame[data_frame.end != " "]

    # convert to dict
    data_frame = data_frame.to_dict(orient='records')

    events = []
    for i, frame in enumerate(data_frame):

        # convert start/end time + timezone to dict
        start_dict = {'dateTime': frame['start'], 'timeZone': frame['timezone']}
        end_dict = {'dateTime': frame['end'], 'timeZone': frame['timezone']}

        frame['start'] = start_dict
        frame['end'] = end_dict
        # delete timezone from data_frame
        del frame['timezone']

        if frame['organizer'] != " ":
            frame['organizer'] = {'email': frame['organizer'], 'self': True}

        attendees = []
        if frame['attendees'] != " ":
            emails = frame['attendees'].split('\n')
            for j in emails:
                attendees.append({'email': j})
        frame['attendees'] = attendees

        rec_rule = []
        if frame['recurrence'] != " ":
            if frame['how often']:
                rec = frame['recurrence'].lower().strip()
                if rec == 'weekly':
                    rec_rule = ["RRULE:FREQ=WEEKLY;"]
                elif rec == 'daily':
                    rec_rule = ["RRULE:FREQ=DAILY;"]
                elif rec == 'monthly':
                    rec_rule = ["RRULE:FREQ=MONTHLY;"]
                elif rec == 'yearly':
                    rec_rule = ["RRULE:FREQ=YEARLY;"]
                else:
                    print(f'failed to make event {i} recurring')
            else:
                print(f'need to specify how often the event {i} should be repeated')

        if frame['how often'] != " ":
            if not frame['recurrence'] == " ":
                if isinstance(frame['how often'], int):
                    rec_rule[0] += f"COUNT={frame['how often']}"
        del frame['how often']
        if frame['specify days'] != " ":
            if not frame['recurrence'] == " ":
                rec_rule[0] += f";BYDAY={frame['specify days']}"
        del frame['specify days']

        frame['recurrence'] = rec_rule
        events.append(frame)
    return events
