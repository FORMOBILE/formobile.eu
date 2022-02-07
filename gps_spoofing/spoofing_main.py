"""
Main module to start GPS spoofing
"""
import sys
import threading
import time
import json

from working import is_working
from enjoying import is_enjoying
from definitions import CONFIG_PATH
from ppadb.device import Device
from ppadb.client import Client
from weekend import is_weekend, weekend


def location_spoofer(arg: str, dev: Device, lat, long):
    """
    Start or stop the location spoofing app, called Appium Settings

    :param arg: download or delete
    :param dev: connected device
    :param lat: latitude of the place
    :param long: longitude of the place
    :return: Nothing
    """
    if arg == ('start' or 'Start' or 'START'):
        # Open app
        dev.shell('monkey -p io.appium.settings 1')
        # Changing location for newer android versions
        dev.shell('am start-foreground-service --user 0 -n io.appium.settings/.LocationService '
                  f'--es longitude {str(long)} '
                  f'--es latitude {str(lat)}')
        # Changing location for older android versions
        dev.shell('am startservice --user 0 -n io.appium.settings/.LocationService '
                  f'--es longitude {str(long)} '
                  f'--es latitude {str(lat)}')
        # Opens Google Maps to log the location
        dev.shell('monkey -p com.google.android.apps.maps 1')
        print(f'Location spoofing activated on {dev.serial}.')
        print(f'Device is located at longitude: {long} and latitude: {lat}')
        time.sleep(15)
    elif arg == ('stop' or 'Stop' or 'STOP'):
        # Stop previous location spoofing
        dev.shell('am stopservice io.appium.settings/.LocationService')
        print(f'Location spoofing deactivated on {dev.serial}.')
    else:
        print('ERROR: Given command is not defined. Please try again.')


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

threads = []

while True:
    for i, d in enumerate(devices):
        device = devices[i]
        for j in range(len(config['People'])):
            if config['People'][j]['Mobile devices'][0]['Serial number'] == device.serial:
                person = config['People'][j]
                pers = person['Mobile devices'][0]
                # True, if it's weekend
                if is_weekend():
                    # True, if it's time for weekend activity
                    if weekend(person):
                        latitude = pers['weekend activity location']['latitude']
                        longitude = pers['weekend activity location']['longitude']
                    # True, if it's time to go home
                    else:
                        latitude = pers['home location']['latitude']
                        longitude = pers['home location']['longitude']
                # True, if it's work time
                elif is_working(person):
                    latitude = pers['work location']['latitude']
                    longitude = pers['work location']['longitude']
                # True, if it's after work time
                elif is_enjoying(person):
                    latitude = pers['spare time location']['latitude']
                    longitude = pers['spare time location']['longitude']
                # True, if it's time to go home
                else:
                    latitude = pers['home location']['latitude']
                    longitude = pers['home location']['longitude']
                # Possible arguments are: start, stop
                t = threading.Thread(target=location_spoofer, args=('start', device, latitude, longitude))
                t.start()
                threads.append(t)
    for t in threads:
        t.join()
    # Location is refreshed every 30 minutes
    time.sleep(1800)
