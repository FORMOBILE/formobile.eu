"""
Module to set up a gmail token
"""
import logging
import os
import ezgmail


CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

def setup_mail(sender_token: str) -> None:
    """
    Checks for token file in the specified directory.
    If the token does not exist yet, the google oauth screen will be opened and the user must log in.
    The token is then stored in the specified path.

    In order to use this function the credentials.json must be in the same folder.
    Steps to get the credentials.json file:
        - Create a new project on Google Cloud Console
        - add the Google Calendar API via the API menu
        - configure OAuth Consent Screen
        - download credentials from Credentials menu
            - must be renamed to credentials.json
        For more detailed instructions: https://support.google.com/cloud/answer/6158849?hl=en

    :param sender_token: path to token
    :return: Nothing
    """
    ezgmail.init(tokenFile=sender_token, credentialsFile=CREDENTIALS_FILE)
    logging.info(f'ezgmail initiated with token: {os.path.basename(sender_token)}')
