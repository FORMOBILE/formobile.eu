"""
Module to remove metadata from pictures
"""
import logging
import os

# from PIL import Image


count_deleted_images = 0
src = ''
dst = ''
logging.info('Start removing pictures with metadata...')
for pic in os.listdir(src):
    try:
        # "Removes" metadata by opening the image and saving it
        # image = Image.open(f'{pic}')
        # image.save(dst + pic)

        # Removes metadata with exiftool
        os.popen(f'exiftool -all= {src + pic}')
    except:
        logging.info('Could not save picture.')
        count_deleted_images += 1
logging.info(f'Removed {count_deleted_images} pictures from data set successfully.')
logging.info('No pictures with metadata left.')
