"""
Module for important definitions
"""
import json
import logging
import os

import pandas as pd

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
)

PICTURES_PATH = os.path.join(os.path.expanduser('~'), 'pictures')
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(ROOT_DIR, 'config.json')
CHROMEDRIVER = os.path.join(ROOT_DIR, 'chromedriver')
DATASETS = os.path.join(ROOT_DIR, 'datasets')

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

open_conversations = []
open_emails = []

CREDENTIALS_FILE = os.path.join(os.path.dirname(__file__), 'gmail', 'credentials.json')

# prepare_datasets.py generates messages_emoji.json from train.json
AMAZON_DATA = os.path.join(os.path.dirname(__file__), 'datasets', 'amazon', 'messages_emoji.json')
one_on_one_conv = pd.read_json(AMAZON_DATA)
REDDIT_DATA = []
group_chats = []
"""
for i, j in enumerate(config["Whatsapp groups"]):
    REDDIT_DATA.append(os.path.join(ROOT_DIR, config["Whatsapp groups"][i]["group_conversation_path"]))
    group_chats.append(pd.read_json(REDDIT_DATA[i]))
"""

CONVERSATIONS_JSON = os.path.join(ROOT_DIR, 'messenger', 'whatsapp', 'conversations.json')

objects = []

"""
EMAIL_DATA = os.path.join(os.path.dirname(__file__), 'datasets', 'SeriousConversation', 'email_dataset.json')
emails = pd.read_json(EMAIL_DATA)
"""
groups = config['Whatsapp groups']

possible_group_conversations = []

if os.path.exists(CONVERSATIONS_JSON):
    logging.info('Loading conversations of the last run')
    with open(CONVERSATIONS_JSON, 'r') as f:
        state_data = json.load(f)
    for conv in state_data['conversations']:
        if conv:
            open_conversations.append(pd.DataFrame(conv))
    for mail in state_data['email conversations']:
        if mail:
            open_emails.append(pd.DataFrame(mail))
    possible_conversations = state_data['possible chats']
    possible_group_conversations = state_data['possible group chats']
    possible_email_conversations = state_data['possible emails']
    logging.info('Loaded conversations of the last run')
else:
    logging.info('No previous run found - Loading new Data')
    possible_conversations = list(one_on_one_conv.keys())
    #for i, j in enumerate(config["Whatsapp groups"]):
    #    possible_group_conversations.append(list(group_chats[i].keys()))
    #possible_email_conversations = list(emails.keys())
