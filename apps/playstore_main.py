import json
import os.path
import time
import sys

from definitions import CONFIG_PATH, ROOT_DIR
from ppadb.client import Client


with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

for i, dev in enumerate(devices):
    device = devices[i]
    for j in range(len(config['People'])):
        if config['People'][j]['Mobile devices'][0]['Serial number'] == device.serial:
            x = config['People'][j]['Mobile devices'][0]['x coordinate']
            y = config['People'][j]['Mobile devices'][0]['y coordinate']
            person = config['People'][j]['Mobile devices'][0]['Whatsapp token']
            filepath = os.path.join(ROOT_DIR, 'datasets', 'apps', f'apps_{person}')
            with open(filepath) as fp:
                # Reads the first line from the apps file
                line = fp.readline()
                while line:
                    app_package = line.strip()
                    print(app_package)
                    # Opens the Google Play Store on the device and searches for the app
                    device.shell(f'am start market://details?id={app_package}')
                    time.sleep(3)
                    device.shell(f'input tap {x} {y}')
                    time.sleep(3)
                    # Reads the following line
                    line = fp.readline()
