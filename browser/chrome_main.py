"""
Main Module to generate a Google Chrome browser history
"""
import threading
import json
import sys
import os

from ppadb.client import Client
from definitions import CONFIG_PATH, DATASETS
from populate import populate
# from populate import populate_random


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

threads = []

for i, dev in enumerate(devices):
    device = devices[i]
    for j in range(len(config['People'])):
        if config['People'][j]['Mobile devices'][0]['Serial number'] == device.serial:
            # Checks which person's (PERSON_A, ...) device
            person = config['People'][j]['Mobile devices'][0]['Whatsapp token']
            filepath = os.path.join(DATASETS, 'browser', f'{person}')

            # Visit every website from list
            t = threading.Thread(target=populate, args=(filepath, device))

            # Visit some random websites from list
            # t = threading.Thread(target=populate_random, args=(filepath, device, 3))

            t.start()
            threads.append(t)

for t in threads:
    t.join()
