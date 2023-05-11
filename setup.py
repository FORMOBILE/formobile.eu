"""
Module to set up all tokens
"""
import json
import logging
import os

from definitions import CONFIG_PATH
from gmail.setup_mail import setup_mail
from google_calendar.cal_setup import get_calendar_service
from messenger.whatsapp_setup import whatsapp_setup

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
    filename='example.log'
)

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Set up google calendar token
logging.info('Starting to generate google calendar token')
for i, person in enumerate(config['People']):
    for j, account in enumerate(person['Gmail account']):
        print('choose: ', person['First name'], person['Surname'])
        path = os.path.join(os.path.dirname(__file__), 'Token', person['Mobile devices'][0]['Whatsapp token'])
        if not os.path.exists(path):
            os.mkdir(path)
        calendar_path = os.path.join(path, account['Calendar token'])
        get_calendar_service(calendar_path)
        logging.info(f'Generated {account["Calendar token"]}')
logging.info('Finished generating google calendar token')

# Set up google mail token
logging.info('Starting to generate google mail token')
for i, person in enumerate(config['People']):
    for j, account in enumerate(person['Gmail account']):
        print('choose: ', person['First name'], person['Surname'])
        path = os.path.join(os.path.dirname(__file__), 'Token', person['Mobile devices'][0]['Whatsapp token'])
        if not os.path.exists(path):
            os.mkdir(path)
        mail_path = os.path.join(path, account['Gmail token'])
        setup_mail(mail_path)
        logging.info(f'Gererated {account["Gmail token"]}')
logging.info('Finished generating google mail token')

# Set up Whatsapp Cookies
logging.info('Starting to generate Whatsapp token')
for i, person in enumerate(config['People']):
    for j, device in enumerate(person['Mobile devices']):
        print('scan for: ', person['First name'], person['Surname'])
        driver = whatsapp_setup(device['Whatsapp token'])
        driver.close()
        logging.info(f'Generated Whatsapp token for {person["First name"]} {person["Surname"]}')
logging.info('Finished generating Whatsapp token')
