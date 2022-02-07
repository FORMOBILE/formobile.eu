"""
Module to install apks on android devices
"""
import logging
import os
import traceback

import ppadb
from ppadb.device import Device


def install_apks(directory: str, device: Device) -> None:
    """
    Install all the apks that are stored in the directory on the device.

    Assumption:
                - in the directory are only .apk files stored

    :param directory: directory where the apks are stored
    :param device: device on which the apks should be installed
    :return: Nothing
    """
    for apk in os.listdir(directory):
        app = os.path.join(directory, apk)
        try:
            logging.info(f"{device.serial} is trying to install {apk}")
            device.install(app)
        except ppadb.InstallError:
            logging.warning(f"failed to install {apk} on {device.serial} trying to reinstall the app")
            try:
                device.install(app, reinstall=True)
            except ppadb.InstallError as exc:
                traceback.print_exc()
                logging.warning(f'Exception {exc} occured')


def install_apk(apk: str, device: Device) -> None:
    """
    Installs the specified apk on the device.

    :param apk: path to the apk
    :param device: device on which the apk should be installed
    :return: Nothing
    """
    try:
        logging.info(f"{device.serial} is trying to install {apk}")
        device.install(apk)
    except ppadb.InstallError:
        logging.warning(f"failed to install {apk} on {device.serial} trying to reinstall the app")
        try:
            device.install(apk, reinstall=True)
        except ppadb.InstallError as exc:
            traceback.print_exc()
            logging.warning(f'Exception {exc} occured')
