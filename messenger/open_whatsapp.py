"""
Module to open the WhatsApp window for every person
"""
import json
import os

from whatsapp.whatsapp_setup import whatsapp_setup
from definitions import ROOT_DIR, CONFIG_PATH


with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

for j in range(len(config['People'])):
    person = config['People'][j]['Mobile devices'][0]['Whatsapp token']
    token_dir = os.path.join(ROOT_DIR, 'Token', person)
    whatsapp = whatsapp_setup(os.path.join(token_dir, person), headless=False)
