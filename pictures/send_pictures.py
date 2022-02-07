"""
Module to send pictures to a device
"""
import os

from datetime import datetime
from ppadb.device import Device


def send_pictures(direc: str, dev: Device, naming_conv: str = '%Y%m%d_%H%M%S'):
    """
    Sends all pictures in the directory to the camera folder of the device.

    :param direc: directory where the pictures are stored
    :param dev: device
    :param naming_conv: naming convention for the camera pictures of the phone
    :return:
    """
    for pic in os.listdir(direc):
        file, file_extension = os.path.splitext(os.path.join(direc, pic))
        modification_time = os.path.getmtime(file + file_extension)
        formatted_time = datetime.fromtimestamp(modification_time).strftime("%Y:%m:%d %H:%M:%S")
        filename = datetime.fromtimestamp(modification_time).strftime(naming_conv) + file_extension
        # Changing some of the EXIF data tags
        os.chdir(direc)
        exif_modification = os.popen(f'exiftool -overwrite_original -FileModifyDate="{formatted_time}+02:00" '
                                     f'-ModifyDate="{formatted_time}+02:00" '
                                     f'-DateTimeOriginal="{formatted_time}+02:00" '
                                     f'-CreateDate="{formatted_time}+02:00" '
                                     f'-ImageUniqueID="IMAGE {formatted_time}+02:00" {pic}')
        exif_modification.close()
        # Push to camera
        dev.push(file + file_extension, f"/sdcard/DCIM/Camera/{filename}")
        # Refresh the sdcard
        dev.shell(
            f'am broadcast -a android.intent.action.MEDIA_SCANNER_SCAN_FILE -d file:///sdcard/DCIM/Camera/{filename}')
