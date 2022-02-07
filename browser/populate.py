"""
Module to populate the Google Chrome browser history
"""
import random
import time

from ppadb.device import Device


def populate(filepath: str, dev: Device):
    """
    Populates the browsing history via the given text file. Every website given will be opened.
    The websites defined in the file should have 'http' and 'www' explicitly declared, for example:
    http://www.paste_your_website.com


    :param filepath: text file with every website on a new line
    :param dev: device
    :return: Nothing
    """
    with open(filepath) as fp:
        # Reads the first line from the browser history file
        line = fp.readline()
        while line:
            website = line.strip()
            # Opens Chrome on the device and searches for the website
            dev.shell(f'am start -a "android.intent.action.VIEW" -d "{website}" '
                         f'--es "com.android.browser.application_id" "com.android.chrome"')
            time.sleep(3)
            # Reads the following line
            line = fp.readline()


def populate_random(filepath: str, dev: Device, number_of_sites: int):
    """
    Populates the browsing history via the given text file. Only a random number of websites given will be opened.
    The websites defined in the file should have 'http' and 'www' explicitly declared, for example:
    http://www.paste_your_website.com


    :param filepath: text file with every website on a new line
    :param dev: device which browsing history should be populated
    :param number_of_sites: the number of random sites
    :return: Nothing
    """
    count = 0
    counter = 0
    while counter < number_of_sites:
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                count += 1
                website = line.strip()
                line = fp.readline()
            rand = random.randint(1, count)
            count = 0
        with open(filepath) as fp:
            line = fp.readline()
            while line:
                count += 1
                website = line.strip()
                line = fp.readline()
                if count == rand:
                    dev.shell(f'am start -a "android.intent.action.VIEW" -d "{website}" '
                              f'--es "com.android.browser.application_id" "com.android.chrome"')
                    time.sleep(3)
            count = 0
        counter += 1
