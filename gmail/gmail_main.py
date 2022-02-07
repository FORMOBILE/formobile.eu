"""
gmail main module
"""
import json
import logging
import os

from start_mailing import start
from definitions import CONFIG_PATH
from gmail_account import EmailAccount



logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
)

# Credentials file is from the Google Cloud Platform and is needed for the Gmail API
CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')

with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

# Setting up email conversation partners
PERSON_A = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_A/morley_gmail.json',
    config['People'][0]['Gmail account'][0]['Gmail address'],
    config['People'][0]['First name'],
    config['People'][0]['Gmail account'][0]['Signature'],
    config['People'][1]['Gmail account'][0]['Gmail address']
)

PERSON_B = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_B/worthington_gmail.json',
    config['People'][1]['Gmail account'][0]['Gmail address'],
    config['People'][1]['First name'],
    config['People'][1]['Gmail account'][0]['Signature'],
    config['People'][0]['Gmail account'][0]['Gmail address']
)

PERSON_C = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_C/finney_gmail.json',
    config['People'][2]['Gmail account'][0]['Gmail address'],
    config['People'][2]['First name'],
    config['People'][2]['Gmail account'][0]['Signature'],
    config['People'][3]['Gmail account'][0]['Gmail address']
)

PERSON_D = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_D/horton_gmail.json',
    config['People'][3]['Gmail account'][0]['Gmail address'],
    config['People'][3]['First name'],
    config['People'][3]['Gmail account'][0]['Signature'],
    config['People'][2]['Gmail account'][0]['Gmail address']
)

PERSON_E = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_E/craft_gmail.json',
    config['People'][4]['Gmail account'][0]['Gmail address'],
    config['People'][4]['First name'],
    config['People'][4]['Gmail account'][0]['Signature'],
    config['People'][5]['Gmail account'][0]['Gmail address']
)

PERSON_F = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_F/reyna_gmail.json',
    config['People'][5]['Gmail account'][0]['Gmail address'],
    config['People'][5]['First name'],
    config['People'][5]['Gmail account'][0]['Signature'],
    config['People'][4]['Gmail account'][0]['Gmail address']
)

PERSON_G = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_G/lozano_gmail.json',
    config['People'][6]['Gmail account'][0]['Gmail address'],
    config['People'][6]['First name'],
    config['People'][6]['Gmail account'][0]['Signature'],
    config['People'][7]['Gmail account'][0]['Gmail address']
)

PERSON_H = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_H/singh_gmail.json',
    config['People'][7]['Gmail account'][0]['Gmail address'],
    config['People'][7]['First name'],
    config['People'][7]['Gmail account'][0]['Signature'],
    config['People'][6]['Gmail account'][0]['Gmail address']
)

PERSON_I = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_I/sykes_gmail.json',
    config['People'][8]['Gmail account'][0]['Gmail address'],
    config['People'][8]['First name'],
    config['People'][8]['Gmail account'][0]['Signature'],
    config['People'][9]['Gmail account'][0]['Gmail address']
)

PERSON_J = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_J/patton_gmail.json',
    config['People'][9]['Gmail account'][0]['Gmail address'],
    config['People'][9]['First name'],
    config['People'][9]['Gmail account'][0]['Signature'],
    config['People'][8]['Gmail account'][0]['Gmail address']
)

PERSON_K = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_K/hawkins_gmail.json',
    config['People'][10]['Gmail account'][0]['Gmail address'],
    config['People'][10]['First name'],
    config['People'][10]['Gmail account'][0]['Signature'],
    config['People'][11]['Gmail account'][0]['Gmail address']
)

PERSON_L = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_L/leyton_gmail.json',
    config['People'][11]['Gmail account'][0]['Gmail address'],
    config['People'][11]['First name'],
    config['People'][11]['Gmail account'][0]['Signature'],
    config['People'][10]['Gmail account'][0]['Gmail address']
)

PERSON_M = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_M/mohammed_gmail.json',
    config['People'][12]['Gmail account'][0]['Gmail address'],
    config['People'][12]['First name'],
    config['People'][12]['Gmail account'][0]['Signature'],
    config['People'][13]['Gmail account'][0]['Gmail address']
)

PERSON_N = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_N/huffman_gmail.json',
    config['People'][13]['Gmail account'][0]['Gmail address'],
    config['People'][13]['First name'],
    config['People'][13]['Gmail account'][0]['Signature'],
    config['People'][12]['Gmail account'][0]['Gmail address']
)

PERSON_O = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_O/hastings_gmail.json',
    config['People'][14]['Gmail account'][0]['Gmail address'],
    config['People'][14]['First name'],
    config['People'][14]['Gmail account'][0]['Signature'],
    config['People'][15]['Gmail account'][0]['Gmail address']
)

PERSON_P = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_P/hirst_gmail.json',
    config['People'][15]['Gmail account'][0]['Gmail address'],
    config['People'][15]['First name'],
    config['People'][15]['Gmail account'][0]['Signature'],
    config['People'][14]['Gmail account'][0]['Gmail address']
)

PERSON_Q = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_Q/ball_gmail.json',
    config['People'][16]['Gmail account'][0]['Gmail address'],
    config['People'][16]['First name'],
    config['People'][16]['Gmail account'][0]['Signature'],
    config['People'][17]['Gmail account'][0]['Gmail address']
)

PERSON_R = EmailAccount(
    '/home/praktikumslaptop/Schreibtisch/formobile/Token/PERSON_R/tait_gmail.json',
    config['People'][17]['Gmail account'][0]['Gmail address'],
    config['People'][17]['First name'],
    config['People'][17]['Gmail account'][0]['Signature'],
    config['People'][16]['Gmail account'][0]['Gmail address']
)


path1 = '/home/praktikumslaptop/Schreibtisch/subreddit-comments-dl/data/SeriousConversation/20210714153909/'
path2 = '/home/praktikumslaptop/Schreibtisch/subreddit-comments-dl/data/SeriousConversation/20210705073409/'
path3 = '/home/praktikumslaptop/Schreibtisch/subreddit-comments-dl/data/SeriousConversation/20210701085751/'

start(PERSON_A, PERSON_B, PERSON_C, PERSON_D, PERSON_E, PERSON_F, path1,
      PERSON_G, PERSON_H, PERSON_I, PERSON_J, PERSON_K, PERSON_L, path2,
      PERSON_M, PERSON_N, PERSON_O, PERSON_P, PERSON_Q, PERSON_R, path3)
