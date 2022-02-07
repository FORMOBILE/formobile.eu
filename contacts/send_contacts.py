"""
Module to push and save vcards to devices
"""
import logging
import time
import ppadb.device

from uiautomator import Device, JsonRPCError


def send_contacts(filepath: str, device: ppadb.device.Device, contacts_app: str, buttons: list) -> None:
    """
    Sends .vcf files to the phone and saves the contact data.

    Assumptions:
                    - developer options and usb debugging are activated
                    - phone is currently unlocked

    Remarks:
                    - gives the contacts_app the right to save and store to storage
                        - worked for HUAWEI Mate 20 lite but not for Samsung A40/ Samsung S9
                        - because it does not work for all phones ui automator is called everytime to press "allow"
                        (LANGUAGE SPECIFIC)

                    - vcards.vcf is first stored on the device and then deleted
                        - I don't know if this file can be restored or leaves any traces

                    - in order to store the contact data a few button presses are made via uiautomator module
                        - these button presses are DEVICE and LANGUAGE SPECIFIC

                    - furthermore uiautomator loads two packages onto the device:
                        - com.github.uiautomator
                        - com.github.uiautomator.test
                        - these two packages are automatically uninstalled by the function
                            - I don't know if these packages can be restored or leave any traces
                        - if these packages exist on the phone before the Device() function is called sometimes the code
                          will not work and throw exceptions

    :param device: device to be populated
    :param contacts_app: device specific contacts app
    :param buttons: buttons that need to be pressed in order to store contacts from .vcf file
    :param filepath: path to the vcard
    :return: nothing
    """

    # grant contacts access to storage
    dev = Device(device.serial)
    logging.info(f'Installed UIAutomator on {device.serial}')
    device.shell(f'adb shell pm grant {contacts_app} android.permission.WRITE_EXTERNAL_STORAGE')
    device.shell(f'adb shell pm grant {contacts_app} android.permission.READ_EXTERNAL_STORAGE')
    logging.info(f'Gave {contacts_app} rw permission for external storage')

    # Via the shell adb push '../formobile/contacts/vcard_data/vcards.vcf'
    # '/sdcard/vcards.vcf'
    device.push(filepath, '/sdcard/vcards.vcf')
    logging.info(f'Loaded vcf file onto {device.serial}')
    device.shell(
        f'am start -t "text/vcard" -d "file:///sdcard/vcards.vcf" -a android.intent.action.VIEW {contacts_app}')
    logging.info('Imported contacts from vcf file')

    try:
        logging.info(f'trying to allow contacts app of {device.serial} to access photos media and files')
        dev(text="Allow").click(timeout=15)
        logging.info(f'successfully clicked "Allow" on screen of {device.serial}')
    except JsonRPCError:
        logging.warning(f"{device.serial} may not have gotten the permissions to import the vcard")

    try:
        for button in buttons:
            dev(text=f"{button}").click()
            logging.info(f'Clicked {button} on {device.serial}')
        logging.info(f'Saved contacts on {device.serial}')
    except JsonRPCError:
        logging.critical(f'Could not save contacts on {device.serial}, returning to home screen')
        device.shell('input keyevent KEYCODE_HOME')
    # delete app from phone
    device.shell('pm uninstall com.github.uiautomator')
    device.shell('pm uninstall com.github.uiautomator.test')
    logging.info(f'Uninstalled UIAutomator from {device.serial}')

    # delete .vcf file from phone
    # try to eliminate time.sleep - rather wait and check for completion
    time.sleep(10)
    device.shell('rm -r /sdcard/vcards.vcf')
    logging.info(f'Removed vcf file from {device.serial}')
