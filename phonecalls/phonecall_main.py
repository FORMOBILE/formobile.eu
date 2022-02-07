"""
Phone calls main module
"""
import sys
import json
import time

from ppadb.client import Client
from simulate_phone_call import simulate_phone_call
from definitions import CONFIG_PATH


adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

# check for devices
if len(devices) == 0:
    print('no device attached')
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

PERSON_A = adb.device(config['People'][0]['Mobile devices'][0]['Serial number'])
PERSON_B = adb.device(config['People'][3]['Mobile devices'][0]['Serial number'])
PERSON_A_NUMBER = config['People'][0]['Mobile devices'][0]['Phone number']
PERSON_B_NUMBER = config['People'][3]['Mobile devices'][0]['Phone number']


i = 0
while i < 5:
    simulate_phone_call(PERSON_A, PERSON_B, PERSON_B_NUMBER, 10)
    time.sleep(60)
    i = i + 1
