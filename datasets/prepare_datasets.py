"""
Module to prepare the datasets for WhatsApp and email.
"""
import logging
import os
import threading

from datasets import reddit_comments, prepare_email
from datasets.amazon_add_emojis import amazon_add_emojis
from datasets.concat_subreddit_dl_data import concat_data
from definitions import ROOT_DIR

logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
    filename='datasets.log'
)

#### paths to the datasets ####
DATASETS_PATH = os.path.dirname(__file__)
SUBREDDIT_DL = os.path.join(ROOT_DIR, 'subreddit-comments-dl', 'data')

serious = os.path.join(SUBREDDIT_DL, 'SeriousConversation')
pts_serious = os.path.join(DATASETS_PATH, 'SeriousConversation')

casual = os.path.join(SUBREDDIT_DL, 'CasualConversation')
pts_casual = os.path.join(DATASETS_PATH, 'CasualConversation')

pictures_folder = os.path.join(DATASETS_PATH, 'pictures', 'gallery')

amazon_dataset = os.path.join(DATASETS_PATH, 'amazon', 'train.json')

#### code that does the work ####
concat_casual = threading.Thread(target=concat_data, args=(casual, pts_casual))
concat_serious = threading.Thread(target=concat_data, args=(serious, pts_serious))
concat_casual.start()
concat_serious.start()
concat_casual.join()
concat_serious.join()


threads = [threading.Thread(target=amazon_add_emojis, args=(amazon_dataset,)),
           threading.Thread(target=reddit_comments.prepare),
           threading.Thread(target=prepare_email.prepare)]

for thread in threads:
    thread.start()
for thread in threads:
    thread.join()
