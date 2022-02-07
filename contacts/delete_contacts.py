"""
Module to delete all Contacts from device
"""
import logging
import ppadb.device


def delete_contacts(device: ppadb.device.Device, contacts_app: str) -> None:
    """
    Deletes all Contacts from device.

    Assumptions:
                    - developer options and usb debugging are activated
                    - phone is currently unlocked

    Remarks:
                    - tries to give the contacts_app the right to save and store to storage
                        - worked for HUAWEI Mate 20 lite but not for Samsung A40
                        - otherwise the user would have to allow the access manually
                    - Removes call logs as well


    :param contacts_app: contacts app of device
    :param device: device whose contacts should be deleted
    :return: Nothing
    """

    device.shell(f'adb shell pm grant {contacts_app} android.permission.WRITE_EXTERNAL_STORAGE')
    device.shell(f'adb shell pm grant {contacts_app} android.permission.READ_EXTERNAL_STORAGE')

    device.shell(f'pm clear {contacts_app}')
    logging.info(f'Deleted all contacts from {device.serial}')
