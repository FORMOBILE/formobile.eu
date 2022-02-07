"""
Module to get a list of all the moderators of a subreddit
"""
import json
import logging
import requests

from typing import List


def get_mods(subreddit: str):
    """
    Uses a Reddit bot to get a list of all the moderators of a subreddit.

    Needs an active internet connection!

    :param subreddit: the subreddit to get the modlist from
    :return: list of moderators
    """
    # Reddit bot ID and secret
    auth = requests.auth.HTTPBasicAuth('3vSvZB2gOve0O9gXDIJmKA', '378ADi_D0Q6O2By87XUv5_2wWm58eQ')
    # Here we pass our username and password
    data = {'grant_type': 'password',
            'username': 'OurBotAccount',
            'password': 'wilhelmborange1D'}
    # Setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'ModeratorGetter/0.0.1'}
    # Send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token', auth=auth, data=data, headers=headers)
    # Convert response to JSON and pull access_token value
    token = res.json()['access_token']
    # Add authorization to our headers dictionary
    headers = {**headers, **{'Authorization': f"bearer {token}"}}
    # While the token is valid (~2 hours) we just add headers=headers to our requests
    requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

    moderator_names = []
    res = requests.get(f"https://oauth.reddit.com/r/{subreddit}/about/moderators.json", headers=headers)
    for mod in res.json()['data']['children']:
        moderator_names.append(mod['name'])
    logging.info('Created Moderator list from web')

    return moderator_names


# pylint: disable = invalid-name
def get_mods_from_file(file: str) -> List[str]:
    """
    Reddit seems to sometimes detect automated software and refuses access to the data.
    In such cases the .json has to be downloaded manually from:
        https://www.reddit.com/r/<subreddit name>/about/moderators.json

    This method formats the data the same way as the one that uses selenium
    :param file: path to the moderators json file
    :return: list of moderators
    """
    with open(file, 'r') as f:
        mods = json.load(f)
    moderator_names = []
    for mod in mods['data']['children']:
        moderator_names.append(mod['name'])
    logging.info(f'Created Moderator list from file {file}')

    return moderator_names
