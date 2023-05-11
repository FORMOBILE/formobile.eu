"""
Module for a class that represents gmail accounts
"""
import logging
import os
import random
import time
import ezgmail
import pandas as pd

from difflib import SequenceMatcher
from typing import List


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z',
)

CREDENTIALS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials.json')


class EmailAccount:
    """
    Class that represents a Gmail account
    """

    def __init__(self, token: str, email_address: str, name: str, signature: str, email_partners: dict):
        self.token = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Token', token)
        self.email_address = email_address
        self.name = name
        self.signature = signature
        self.email_partners = email_partners

    def reply_unread_msgs(self, data: pd.DataFrame, init_sender: object = None, max_results=25):
        """
        Checks for unread messages and answers them if there is a reply in the data

        :param data: data in the form of a pandas DataFrame from which the reply is read
        :param init_sender: sender of the initial message - is used for the salutation, if present
        :param max_results: maximal number of unread messages that will be read
        :return: Nothing
        """
        logging.info(f'Initiating {self.token}')
        ezgmail.init(tokenFile=self.token, credentialsFile=CREDENTIALS_FILE)
        mails = ezgmail.unread(maxResults=max_results)
        for msg in mails:
            incoming_message = msg.messages[0]
            for _, row in data.iterrows():
                # Check if incoming message has an answer listed in df
                if SequenceMatcher(None, row['previous message'],
                                   incoming_message.body.replace("\n", "\\n")).ratio() > 0.7:
                    logging.info(f"{self.email_address} is replying to {msg.snippet} from {msg.senders()}")
                    if init_sender:
                        salut = f'Dear {init_sender.name}\n\n'
                    else:
                        salut = 'Hello\n\n'
                    reply_body = salut + row['body'] + f"\n\n{self.signature}"
                    time.sleep(1)
                    incoming_message.reply(reply_body)
                    logging.info(f"{self.email_address} sent message: {reply_body}")
            incoming_message.markAsRead()

    # pylint: disable=invalid-name
    def send_mail(self, recipient: str, subject: str, text: str, cc="", bcc="",
                  attachments: list = None) -> None:
        """
        Sends an email to the specified arguments
        :param recipient: Recipient of the email
        :param subject: Subject of the email
        :param text: Text of the email
        :param cc: recipient of carbon copy of the email - empty by default
        :param bcc: recipient of blind carbon copy of the email - empty by default
        :param attachments: List of filepaths (str) to attachments for the email
        :return: Nothing
        """
        logging.info(f'Initiating {self.token}')
        ezgmail.init(tokenFile=self.token, credentialsFile=CREDENTIALS_FILE)
        ezgmail.send(recipient, subject, text, attachments, cc, bcc)
        logging.info(f'Message sent: from: {os.path.basename(self.token)} subject: {subject}, text: {text}, '
                     f'attachments: {attachments}, cc: {cc}, bcc: {bcc}')

    def reply_unread_msg(self, data: List[pd.DataFrame], typespeed=0.25) -> None:
        """
        Replies to one unread message if an answer is available.
        :param data: email DataFrame
        :param typespeed: typing speed
        :return: Nothing
        """
        logging.info(f'Initiating {self.token}')
        ezgmail.init(tokenFile=self.token, credentialsFile=CREDENTIALS_FILE)
        mails = ezgmail.unread(maxResults=1)
        if mails:
            incoming_message = mails[0].messages[0]
            for df in data:
                # Check if incoming message has an answer listed in df
                if SequenceMatcher(None, df['previous message'].iloc[0],
                                    incoming_message.body.replace("\n", "\\n")).ratio() > 0.7:
                    logging.info(f"{self.email_address} is replying to "
                                 f"{incoming_message.snippet} from {incoming_message.senders()}")
                    salut = self.email_partners.get(incoming_message.senders()[0])
                    reply_body = salut + df['body'].iloc[0] + f"\n\n{self.signature}"
                    time.sleep(len(reply_body.split()) * typespeed + random.uniform(0, 5))
                    incoming_message.reply(reply_body)
                    logging.info(f"{self.email_address} sent message: {reply_body}")
                    incoming_message.markAsRead()
                    break
            incoming_message.markAsRead()
        else:
            return
        return