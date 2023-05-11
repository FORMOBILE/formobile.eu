"""
pictures main module
"""
import os
import logging
import json
import threading
import sys

from datetime import datetime
from ppadb.client import Client
from send_pictures import send_pictures
from move_pictures_to_folder import move_pictures_to_folder
from definitions import ROOT_DIR, CONFIG_PATH, PICTURES_PATH
from datasets.modify_timestamps import modify_timestamps


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Source path is a copy of the original data set, because original data set should not be modified
src_path = PICTURES_PATH
# Path is the directory where the serial number folders are stored
path = os.path.join(ROOT_DIR, 'datasets', 'pictures', 'gallery')
# Important for the threading process later
threads = []

for i, dev in enumerate(devices):
    device = devices[i]

    for j in range(len(config['People'])):

        if config['People'][j]['Mobile devices'][0]['Serial number'] == device.serial:
            full_path = os.path.join(path, device.serial)
            os.chdir(path)
            if os.path.isdir(full_path):
                # If folder exists, it deletes the content of it
                delete = os.popen(f'rm -r {device.serial}')
                os.wait()
                delete.close()

                create = os.popen(f'mkdir {device.serial}')
                os.wait()
                create.close()
            else:
                # If folder does not exist, it creates one
                create = os.popen(f'mkdir {device.serial}')
                os.wait()
                create.close()

            # Copies the right amount of pictures to the destination path on this PC
            dst_path = os.path.join(path, device.serial)
            number_of_pics = config['People'][j]['Mobile devices'][0]['nr of pics']
            move_pictures_to_folder(src_path, dst_path, number_of_pics)

            # Modifies and randomizes the timestamps as given in the config.json
            dev = config['People'][j]['Mobile devices'][0]
            start = datetime.strptime(dev['timeframe start'], '%Y-%m-%dT%H:%M:%S')
            end = datetime.strptime(dev['timeframe end'], '%Y-%m-%dT%H:%M:%S')
            modify_timestamps(dst_path, start, end)

            # Stores the naming convention of each device defined in the config.json
            string_format = config[f"{device.shell('getprop ro.product.model')}".strip()]['Photo names']

            logging.info(f'Start sending pictures to {device.serial}...')
            # Sends the pictures to the device
            # Threading is implemented to parallelize the sending process and save time
            t = threading.Thread(target=send_pictures, args=(dst_path, device, string_format))
            t.start()
            threads.append(t)


for t in threads:
    t.join()

logging.info(f'Pictures transferred successfully')
