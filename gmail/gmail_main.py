"""
gmail main module
"""
import json
import logging
import os

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

accounts = []

# Setting up email conversation partners

for person in config['People']:
    token_dir = person['Mobile devices'][0]['Whatsapp token']
    token_name = person['Gmail account'][0]['Gmail token']
    accounts.append(EmailAccount(
        #os.path.join(ROOT_DIR, 'Token', token_dir, token_name),
        os.path.join(token_dir, token_name),
        person['Gmail account'][0]['Gmail address'],
        person['First name'],
        person['Gmail account'][0]['Signature'],
        person['Gmail account'][0]['Email partners'])
    )

# every account sends a message to every account listed in their email partners section.
for account in accounts:
    partner = account.email_partners
    partner_emails = list(partner.keys())
    for email in partner_emails:
        """
        
        IMPLEMENT YOUR DATASETS HERE
        
        """
        body = f'{account.email_partners[email]}\n\n' + 'test'.replace("\\n", "\n") + f"\n\n{account.signature}"
        account.send_mail(email, 'title', body)
