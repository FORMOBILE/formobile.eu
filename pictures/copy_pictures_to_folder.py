"""
Module to copy pictures.
"""
import logging
import os
import random

from shutil import copy2


def copy_pictures_to_folder(from_folder: str, to_folder: str, amount: int) -> None:
    """
    Copies a given amount of random pictures from from_folder to to_folder and deletes them from from_folder to avoid
    duplicates.

    :param from_folder: path to folder where the picture dataset is stored
    :param to_folder: path to where the sample should be stored
    :param amount: amount
    :return: Nothing
    """
    # Takes a random sample of pictures
    pictures = random.sample(os.listdir(from_folder), amount)
    logging.info(f'Taking a random sample of {amount} pictures from the dataset {from_folder}')
    for pic in pictures:
        src = os.path.join(from_folder, pic)
        dst = os.path.join(to_folder, pic)
        # Copying
        copy2(src, dst)
        logging.info(f'Copied {src} to {dst}')
        # Deleting
        os.remove(src)
