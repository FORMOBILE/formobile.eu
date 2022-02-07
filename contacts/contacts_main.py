"""
Module to push contacts to the device
"""
import json
import logging
import os
import sys
import threading
import time
import pandas as pd

from ppadb.client import Client
from contacts.send_contacts import send_contacts
from contacts.delete_contacts import delete_contacts
from contacts.vcard_data import v_card
from definitions import CONFIG_PATH


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Set up contacts
PATH_TO_VCARD_DATA = os.path.join(os.path.dirname(__file__), 'vcard_data')
PATH_TO_VCARD_CSV = os.path.join(PATH_TO_VCARD_DATA, 'vcard_data.csv')

df = pd.read_csv(PATH_TO_VCARD_CSV, dtype={'plz': 'str', 'phone_h': 'str', 'phone_w': 'str'})

'''
# Add all people from config.json file to vcard_data.csv
logging.info('Started to add contacts from the config file')
for i, person in enumerate(config['People']):
    row = []
    row.extend(
        [person['First name'], person['Surname'], person['Birthday'], person['Organisation'], person['Home phone']])
    row.append(person['Mobile devices'][0]['Phone number'])
    row.extend([person['Street'], person['Postal code'], person['City']])
    row.append(person['Gmail account'][0]['Gmail address'])
    df2 = pd.DataFrame([row],
                       columns=['first_names', 'last_names', 'birthday', 'orgs', 'phone_h', 'phone_w', 'street', 'plz',
                                'city', 'email'])
    logging.info(f'Added {df2["first_names"]} {df2["last_names"]} to contacts dataframe')
    df = df.append(df2, ignore_index=True)
'''

# Format birthdays to date s.t. vcard recognizes them
df['birthday'] = pd.to_datetime(df['birthday'])

PATH_TO_FINAL_VCARD_CSV = os.path.join(PATH_TO_VCARD_DATA, 'vcard_data_with_config.csv')

# Creates the final csv file, called vcard_data_with_config.csv
df.to_csv(PATH_TO_FINAL_VCARD_CSV, index=False)
logging.info('Finished adding contacts from config file')
logging.info(f'Saved final contacts csv in {PATH_TO_FINAL_VCARD_CSV}')

PATH_TO_VCARD = os.path.join(PATH_TO_VCARD_DATA, 'vcards.vcf')
vcards = v_card.generate_vcards(PATH_TO_FINAL_VCARD_CSV, PATH_TO_VCARD)
logging.info(f'Saved the final vcard in {PATH_TO_VCARD}')


logging.info('Starting to load contact onto the devices')
threads = []
for i, dev in enumerate(devices):
    device = devices[i]
    for j in range(len(config['People'])):
        person = config['People'][j]
        if person['Mobile devices'][0]['Serial number'] == device.serial:
            model = person['Mobile devices'][0]['Model']
            delete_contacts(device, config[model]['Contacts delete'])
            time.sleep(2)
            t = threading.Thread(target=send_contacts, args=(PATH_TO_VCARD, device, config[model]['Contacts store'],
                                                             config[model]['Buttons contacts']))
            t.start()
            threads.append(t)
for t in threads:
    t.join()

logging.info('Finished loading contact onto the devices')
