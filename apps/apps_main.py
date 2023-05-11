"""
apps main module
"""
import os
import threading
import ppadb.device
import json

from definitions import CONFIG_PATH
from apps.copy_apps_to_folder import copy_apps_to_folder
from ppadb.client import Client
from apps.install_apks import install_apks


with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()


def setup_apps(device: ppadb.device.Device) -> None:
    path = os.path.join(os.path.dirname(__file__))
    std_apps = os.path.join(path, '../datasets/apps/standard')

    # Installs all standard applications to all connected devices
    install_apks(std_apps, device)

    for person, other in enumerate(['People']):
        nr_of_ind_apps = config['People'][person]['Mobile devices'][0]['individual apks']
        if nr_of_ind_apps != 0:
            individual_apks = os.path.join(path, device.serial)
            if os.path.exists(individual_apks):
                install_apks(individual_apks, device)
            else:
                # to do change install apks s.t. apps do not need to be copied --> way less storage usage
                os.mkdir(individual_apks)
                copy_apps_to_folder(os.path.join(path, '../datasets/apps/individual'), individual_apks,
                                    nr_of_ind_apps)
                install_apks(individual_apks, device)


threads = [threading.Thread(target=setup_apps, args=(dev,)) for dev in devices]
for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
