"""
Module to copy files
"""
import logging
import os
import random
from shutil import copy2


def copy_apps_to_folder(from_folder: str, to_folder: str, amount: int) -> None:
    """
    Copies an amount of random apps from from_folder to to_folder.

    :param from_folder: folder of files to be copied
    :param to_folder: destination folder
    :param amount: amount of random apps
    :return: Nothing
    """
    apps = random.sample(os.listdir(from_folder), amount)
    logging.info(f'Taking a random sample of {amount} apps from {from_folder}')
    for app in apps:
        src = os.path.join(from_folder, app)
        dst = os.path.join(to_folder, app)
        copy2(src, dst)
        logging.info(f'Copied {src} to {dst}')
