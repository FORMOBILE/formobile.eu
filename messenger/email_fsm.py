"""
Email branch of modular fsm.

!!! doesn't work properly and is not finished/ pylint checked !!!
"""
import logging
import os
import random
import time
import traceback

import numpy as np
import pandas as pd

from definitions import possible_email_conversations, emails, open_emails, ROOT_DIR
from gmail.gmail_account import EmailAccount


def prime(fun):
    """
    Used as an decorator in order to make the functions reach the yield statement and thus initiate the states.
    :param fun: function to be primed
    :return: Nothing
    """

    def wrapper(*args, **kwargs):
        var = fun(*args, **kwargs)
        var.send(None)
        return var

    return wrapper


class EmailFSM:
    """
    Class for email branch.
    """

    def __init__(self, person_details: dict, trans_matrix: np.ndarray,
                 typespeed: float = 0.4):
        """
        Initializes all the attributes for the person and opens WhatsApp Web for their phone (only if non headless), as
        well as an EmailAccount object from which emails are sent.

        :param person_details: dict of person details as they are in the config file
        :param trans_matrix: transition matrix for that person
        :param typespeed: how fast does that person type - measured in words per second
        :param active_hours:
        """
        self.token_dir = os.path.join(ROOT_DIR, 'Token', person_details['Mobile devices'][0]['Whatsapp token'])
        self.token = person_details['Mobile devices'][0]['Whatsapp token']
        self.name = person_details['First name'] + " " + person_details['Surname']

        self.wps = typespeed

        self.email = EmailAccount(
            os.path.join(self.token_dir, person_details['Gmail account'][0]['Gmail token']),
            person_details['Gmail account'][0]['Gmail address'],
            person_details['First name'],
            person_details['Gmail account'][0]['Signature'],
            person_details['Gmail account'][0]['Email partners']
        )

        self.trans_matrix = trans_matrix

        self.idle_email = self._create_idle()

        # email states
        self.read_mail = self._create_read_mail()
        self.write_mail = self._create_write_mail()

        self.stopped = False

    def get_idle(self):
        """
        getter for idle state.
        :return:
        """
        return self._create_idle

    @prime
    def _create_idle(self) -> None:
        """
        Creates the "idle email" state for the email branch of the machine.

        The state itself does nothing and serves only as an entry point to the email branch.
        You can think of it as an "open emails app" command.

        :return: Nothing
        """
        while True:
            char = yield
            if char >= 1 - np.sum(self.trans_matrix[:1, 5]):
                logging.info(f"{self.name} is transferring from idle mail to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:-2, 5]):
                logging.info(f"{self.name} is stays in idle email")
                self.current_state = self.idle_email
            elif char >= 1 - np.sum(self.trans_matrix[:-1, 5]):
                logging.info(f"{self.name} is transferring from idle email to read email")
                self.current_state = self.read_mail
            elif char >= 1 - np.sum(self.trans_matrix[:, 5]):
                logging.info(f"{self.name} is transferring from idle email to write email")
                self.current_state = self.write_mail
            else:
                break

    @prime
    def _create_read_mail(self) -> None:
        """
        Creates the "read email" state for the email branch of the machine.

        Checks if an email has been received and replies to it if theres an answer available
        :return: Nothing
        """
        while True:
            char = yield
            try:
                self.email.reply_unread_msg(open_emails, self.wps)
            except Exception as e:
                logging.warning(f"Exception {e} occurred")
                traceback.print_exc()
            if char >= 1 - np.sum(self.trans_matrix[:-2, 6]):
                logging.info(f"{self.name} is transferring from read email to idle email")
                self.current_state = self.idle_email
            elif char >= 1 - np.sum(self.trans_matrix[:-1, 6]):
                logging.info(f"{self.name} stays in read email")
                self.current_state = self.read_mail
            elif char >= 1 - np.sum(self.trans_matrix[:, 6]):
                logging.info(f"{self.name} is transferring from read email to write email")
                self.current_state = self.write_mail
            else:
                break

    @prime
    def _create_write_mail(self):
        """
        Creates the "write email" state for the email branch of the machine.

        Tries to fetch an initial email from the dataset and sends it.
        :return:
        """
        while True:
            char = yield
            if possible_email_conversations:
                key = random.choice(possible_email_conversations)
                possible_email_conversations.remove(key)
                mail_conv = pd.DataFrame(emails.get(key).get('content'))
                recipient = random.choice(list(self.email.email_partners.keys()))
                salutation = self.email.email_partners.get(recipient)
                body = salutation + mail_conv['body'].iloc[0].replace("\\n", "\n") + f"\n\n{self.email.signature}"
                time.sleep(len(body.split()) * self.wps + random.uniform(0, 10))
                self.email.send_mail(recipient,
                                     subject=mail_conv['previous message'].iloc[0],
                                     text=body)
                mail_conv.drop(mail_conv.index[0], inplace=True)
                if not mail_conv.empty:
                    open_emails.append(mail_conv)

            if char >= 1 - np.sum(self.trans_matrix[:-2, 6]):
                logging.info(f"{self.name} is transferring from write email to idle email")
                self.current_state = self.idle_email
            elif char >= 1 - np.sum(self.trans_matrix[:-1, 6]):
                logging.info(f"{self.name} is transferring from write email to read email")
                self.current_state = self.read_mail
            elif char >= 1 - np.sum(self.trans_matrix[:, 6]):
                logging.info(f"{self.name} stays in write email")
                self.current_state = self.write_mail
            else:
                break
