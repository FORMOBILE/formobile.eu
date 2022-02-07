"""
Setup for google calendar
"""
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
# os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
SCOPES = ["https://www.googleapis.com/auth/calendar"]

CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')


def get_calendar_service(token_file: str) -> object:
    """
    Creates service object from token_file.
    If the token_file doesn't exist yet, the user must log in and one will be created.

    In order to use this function the credentials.json must be in the same folder.
    Steps to get the credentials.json file:
        - Create a new project on Google Cloud Console
        - add the Google Calendar API via the API menu
        - configure OAuth Consent Screen
        - download credentials from Credentials menu
            - must be renamed to credentials.json
        For more detailed instructions: https://support.google.com/cloud/answer/6158849?hl=en


    :param token_file: path to token of the calendar owner
    :return: googleapiclient.discovery.Resource object
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open(token_file, 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)
    return service
