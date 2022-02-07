"""
Module to download/delete GPS spoofing App to device
"""
import sys
import threading
import os

from apps import install_apks
from ppadb.device import Device
from ppadb.client import Client
from definitions import ROOT_DIR


def download_delete(arg: str, dev: Device):
    """
    Download or delete the location spoofing app, called Appium Settings

    :param arg: download or delete
    :param dev: connected device
    :return: Nothing
    """
    if arg == ('download' or 'Download' or 'DOWNLOAD'):
        app_direc = os.path.join(ROOT_DIR, 'settings_apk-debug.apk')
        # Install app
        install_apks.install_apk(app_direc, dev)
        # Give permissions
        dev.shell('appops set io.appium.settings android:mock_location allow')
        dev.shell('pm grant io.appium.settings android.permission.ACCESS_FINE_LOCATION')
        print(f'Spoofer installed successfully on {dev.serial}.')
    elif arg == ('delete' or 'Delete' or 'DELETE'):
        # Uninstall app
        dev.uninstall('io.appium.settings')
        print(f'Spoofer uninstalled successfully on {dev.serial}.')
    else:
        print('ERROR: Given command is not defined. Please try again.')


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

threads = []

for i, d in enumerate(devices):
    device = devices[i]
    # Possible arguments are: download, delete
    t = threading.Thread(target=download_delete, args=('download', device))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
