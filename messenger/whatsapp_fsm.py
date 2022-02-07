"""
WhatsApp branch of the modular fsm.
"""
import logging
import os
import time
import traceback
import random
import numpy as np
import pandas as pd

from ppadb.device import Device
from gps_spoofing.weekend import is_weekend, weekend
from gps_spoofing.working import is_working
from gps_spoofing.enjoying import is_enjoying
from browser.populate import populate, populate_random
from typing import List
from gtts import gTTS
from definitions import possible_email_conversations, emails, open_emails, objects, groups, possible_conversations, \
    possible_group_conversations, one_on_one_conv, group_chats, ROOT_DIR
from definitions import open_conversations as open_conv
from gmail.gmail_account import EmailAccount
from playsound import playsound
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, \
    ElementClickInterceptedException, JavascriptException, InvalidArgumentException, ElementNotInteractableException, \
    MoveTargetOutOfBoundsException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec, ui
from messenger.whatsapp.whatsapp_setup import whatsapp_setup


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


class WhatsappFSM:

    def __init__(self, person_details: dict, dev: Device, trans_matrix: np.ndarray):
        """
        Initializes all the attributes for the person and opens WhatsApp Web for their phone (only if non headless), as
        well as an EmailAccount object from which emails are sent.

        :param person_details: dict of person details as they are in the config file
        :param trans_matrix: transition matrix for that person
        """
        self.person = person_details
        self.token_dir = os.path.join(ROOT_DIR, 'Token', person_details['Mobile devices'][0]['Whatsapp token'])
        self.token = person_details['Mobile devices'][0]['Whatsapp token']
        self.name = person_details['First name'] + " " + person_details['Surname']
        self.conv_partners = person_details['Mobile devices'][0]['Conversation partners']
        self.whatsapp = whatsapp_setup(os.path.join(self.token_dir, self.token), headless=False)
        self.last_contact = None
        self.is_active = True
        self.device = dev
        self.typing_speed = person_details['Mobile devices'][0]['typing speed']
        self.reading_speed = person_details['Mobile devices'][0]['reading speed']
        self.voice_message_probability = person_details['Mobile devices'][0]['voice message probability']
        self.attachment_probability = person_details['Mobile devices'][0]['attachment probability']
        self.home_location = person_details['Mobile devices'][0]['home location']
        self.work_location = person_details['Mobile devices'][0]['work location']
        self.spare_time_location = person_details['Mobile devices'][0]['spare time location']
        self.weekend_activity_location = person_details['Mobile devices'][0]['weekend activity location']
        self.wait = ui.WebDriverWait(self.whatsapp, timeout=120)
        self.email = EmailAccount(
            os.path.join(self.token_dir, person_details['Gmail account'][0]['Gmail token']),
            person_details['Gmail account'][0]['Gmail address'],
            person_details['First name'],
            person_details['Gmail account'][0]['Signature'],
            person_details['Gmail account'][0]['Email partners']
        )
        self.trans_matrix = np.array(trans_matrix)

        # Every state of the finite state machine
        self.idle = self._create_idle()
        self.whatsapp_idle = self._create_whatsapp_idle()
        self.whatsapp_read_message = self._create_whatsapp_read_message()
        self.whatsapp_start_new_chat = self._create_whatsapp_start_new_chat()
        self.whatsapp_send_message = self._create_whatsapp_send_message()
        self.email_idle = self._create_email_idle()
        self.email_read = self._create_email_read()
        self.email_write = self._create_email_write()
        self.mock_location = self._create_mock_location()
        self.browse = self._create_browse()

        self.stopped = False
        self.current_state = self.idle
        objects.append(self)

    def get_idle(self, placeholder=None):
        self.current_state = self.idle
        return self.current_state

    def send(self, char) -> None:
        """
        Sends the char to the current state of the machine.

        :param char: number that should be sent to the machine
        :return: Nothing
        """
        try:
            self.current_state.send(char)
        except StopIteration:
            self.stopped = True

    @prime
    def _create_idle(self) -> None:
        """
        Creates the idle state for the fsm.

        The state itself does nothing and serves only as an entry point to fsm.

        :return: Nothing
        """
        while True:
            char = yield
            if char >= 1 - np.sum(self.trans_matrix[:1, 0]):
                logging.info(f"{self.name} stays in idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:2, 0]):
                logging.info(f"{self.name} is transferring from idle to WhatsApp idle")
                self.current_state = self.whatsapp_idle
            elif char >= 1 - np.sum(self.trans_matrix[:6, 0]):
                logging.info(f"{self.name} is transferring from idle to email idle")
                self.current_state = self.email_idle
            elif char >= 1 - np.sum(self.trans_matrix[:9, 0]):
                logging.info(f"{self.name} is transferring from idle to mock location")
                self.current_state = self.mock_location
            elif char >= 1 - np.sum(self.trans_matrix[:10, 0]):
                logging.info(f"{self.name} is transferring from idle to browse")
                self.current_state = self.browse
            else:
                break

    @prime
    def _create_whatsapp_idle(self) -> None:
        """
        Creates the idle state for the WhatsApp branch of the machine.

        The state itself does nothing and serves only as an entry point to the WhatsApp branch.
        You can think of it as an "open WhatsApp" command.

        :return: Nothing
        """
        while True:
            char = yield
            if char >= 1 - np.sum(self.trans_matrix[:1, 1]):
                logging.info(f"{self.name} is transferring from WhatsApp idle to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:2, 1]):
                logging.info(f"{self.name} stays in WhatsApp idle")
                self.current_state = self.whatsapp_idle
            elif char >= 1 - np.sum(self.trans_matrix[:3, 1]):
                logging.info(f"{self.name} is transferring from WhatsApp idle to WhatsApp read message")
                self.current_state = self.whatsapp_read_message
            elif char >= 1 - np.sum(self.trans_matrix[:4, 1]):
                logging.info(f"{self.name} is transferring from WhatsApp idle to WhatsApp start new chat")
                self.current_state = self.whatsapp_start_new_chat
            elif char >= 1 - np.sum(self.trans_matrix[:5, 1]):
                logging.info(f"{self.name} is transferring from WhatsApp idle to WhatsApp send message")
                self.current_state = self.whatsapp_send_message
            else:
                break

    @prime
    def _create_whatsapp_read_message(self) -> None:
        """
        Creates the "read message" state for the WhatsApp branch of the machine.

        In this state a message from the list of open conversations is read but NOT replied to.

        :return: Nothing
        """
        while True:
            char = yield
            found_conversation = False
            for con in open_conv:
                if con.empty:
                    del con
                elif con['agent'].iloc[0] == self.token:
                    self.read_conversation(con)
                    found_conversation = True
                    break
            if not found_conversation:
                self.read_green_dot()

            if char >= 1 - np.sum(self.trans_matrix[:1, 2]):
                logging.info(f"{self.name} is transferring from WhatsApp read message to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:2, 2]):
                logging.info(f"{self.name} is transferring from WhatsApp read message to WhatsApp idle")
                self.current_state = self.whatsapp_idle
            elif char >= 1 - np.sum(self.trans_matrix[:3, 2]):
                logging.info(f"{self.name} stays in WhatsApp read message")
                self.current_state = self.whatsapp_read_message
            elif char >= 1 - np.sum(self.trans_matrix[:4, 2]):
                logging.info(f"{self.name} is transferring from WhatsApp read message to WhatsApp start new chat")
                self.current_state = self.whatsapp_start_new_chat
            elif char >= 1 - np.sum(self.trans_matrix[:5, 2]):
                logging.info(f"{self.name} is transferring from WhatsApp read message to WhatsApp send message")
                self.current_state = self.whatsapp_send_message
            else:
                break

    @prime
    def _create_whatsapp_start_new_chat(self) -> None:
        """
        Creates the "start new chat" state for the WhatsApp branch of the machine.

        Starts a new chat with a random person that has no open chat with the person.

        If the person has an open conversation with each possible person, a new group chat message is sent with a one
        percent probability.

        :return: Nothing
        """
        while True:
            char = yield
            possible_partners = []
            open_conv_partners = self.get_open_conv_partners()

            for person in self.conv_partners:
                if person not in open_conv_partners and person != self.token:
                    for obj in objects:
                        if person == obj.token:
                            possible_partners.append(obj)

            if len(possible_partners) == 0:
                if groups:
                    possible_groups = []
                    for i, j in enumerate(groups):
                        possible_groups.append(groups[i])
                    rndm = random.randint(0, (len(possible_groups) - 1))
                    # begin a new group conversation where the person is a member of the group
                    try:
                        self.begin_new_group_conversations(
                            random.choice(
                                list({k: v for k, v in possible_groups[rndm].items() if self.token in v}.items())), rndm)
                    except Exception:
                        logging.warning('Message does not exist')
            else:
                self.begin_new_conversation(random.choice(possible_partners))

            if char >= 1 - np.sum(self.trans_matrix[:1, 3]):
                logging.info(f"{self.name} is transferring from WhatsApp start new chat to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:2, 3]):
                logging.info(f"{self.name} is transferring from WhatsApp start new chat to WhatsApp idle")
                self.current_state = self.whatsapp_idle
            elif char >= 1 - np.sum(self.trans_matrix[:3, 3]):
                logging.info(f"{self.name} is transferring from WhatsApp start new chat to WhatsApp read message")
                self.current_state = self.whatsapp_read_message
            elif char >= 1 - np.sum(self.trans_matrix[:4, 3]):
                logging.info(f"{self.name} stays in WhatsApp start new chat")
                self.current_state = self.whatsapp_start_new_chat
            elif char >= 1 - np.sum(self.trans_matrix[:5, 3]):
                logging.info(f"{self.name} is transferring from WhatsApp start new chat to WhatsApp send message")
                self.current_state = self.whatsapp_send_message
            else:
                break

    @prime
    def _create_whatsapp_send_message(self) -> None:
        """
        Creates the "send message" state for the WhatsApp branch of the machine.

        Sends the next message for one conversation in the list of conversations.

        :return: Nothing
        """
        while True:
            char = yield
            for con in open_conv:
                if con.empty:
                    del con
                elif con['agent'].iloc[0] == self.token:
                    self.continue_conversation(con)
                    break

            if char >= 1 - np.sum(self.trans_matrix[:1, 4]):
                logging.info(f"{self.name} is transferring from WhatsApp send message to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:2, 4]):
                logging.info(f"{self.name} is transferring from WhatsApp send message to WhatsApp idle")
                self.current_state = self.whatsapp_idle
            elif char >= 1 - np.sum(self.trans_matrix[:3, 4]):
                logging.info(f"{self.name} is transferring from WhatsApp send message to WhatsApp read message")
                self.current_state = self.whatsapp_read_message
            elif char >= 1 - np.sum(self.trans_matrix[:4, 4]):
                logging.info(f"{self.name} is transferring from WhatsApp send message to WhatsApp start new chat")
                self.current_state = self.whatsapp_start_new_chat
            elif char >= 1 - np.sum(self.trans_matrix[:5, 4]):
                logging.info(f"{self.name} stays in WhatsApp send message")
                self.current_state = self.whatsapp_send_message
            else:
                break

    @prime
    def _create_email_idle(self) -> None:
        """
        Creates the "idle email" state for the email branch of the machine.

        The state itself does nothing and serves only as an entry point to the email branch.
        You can think of it as an "open emails app" command.

        :return: Nothing
        """
        while True:
            char = yield
            if char >= 1 - np.sum(self.trans_matrix[:1, 5]):
                logging.info(f"{self.name} is transferring from email idle to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:6, 5]):
                logging.info(f"{self.name} stays in email idle")
                self.current_state = self.email_idle
            elif char >= 1 - np.sum(self.trans_matrix[:7, 5]):
                logging.info(f"{self.name} is transferring from email idle to email read")
                self.current_state = self.email_read
            elif char >= 1 - np.sum(self.trans_matrix[:8, 5]):
                logging.info(f"{self.name} is transferring from email idle to email write")
                self.current_state = self.email_write
            else:
                break

    @prime
    def _create_email_read(self) -> None:
        """
        Creates the "read email" state for the email branch of the machine.

        Checks if an email has been received and replies to it if theres an answer available

        :return: Nothing
        """
        while True:
            char = yield
            try:
                self.email.reply_unread_msg(open_emails, self.typing_speed)
            except Exception as e:
                logging.warning(f"Exception {e} occurred")
                traceback.print_exc()

            if char >= 1 - np.sum(self.trans_matrix[:1, 6]):
                logging.info(f"{self.name} is transferring from email read to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:6, 6]):
                logging.info(f"{self.name} is transferring from email read to email idle")
                self.current_state = self.email_idle
            elif char >= 1 - np.sum(self.trans_matrix[:7, 6]):
                logging.info(f"{self.name} stays in email read")
                self.current_state = self.email_read
            elif char >= 1 - np.sum(self.trans_matrix[:8, 6]):
                logging.info(f"{self.name} is transferring from email read to email write")
                self.current_state = self.email_write
            else:
                break

    @prime
    def _create_email_write(self):
        """
        Creates the "write email" state for the email branch of the machine.

        Tries to fetch an initial email from the dataset and sends it.

        :return: Nothing
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
                time.sleep(len(body.split()) * self.typing_speed)
                self.email.send_mail(recipient,
                                     subject=mail_conv['previous message'].iloc[0],
                                     text=body)
                mail_conv.drop(mail_conv.index[0], inplace=True)
                if not mail_conv.empty:
                    open_emails.append(mail_conv)

            if char >= 1 - np.sum(self.trans_matrix[:1, 7]):
                logging.info(f"{self.name} is transferring from email write to idle")
                self.current_state = self.idle
            elif char >= 1 - np.sum(self.trans_matrix[:6, 7]):
                logging.info(f"{self.name} is transferring from email write to email idle")
                self.current_state = self.email_idle
            elif char >= 1 - np.sum(self.trans_matrix[:7, 7]):
                logging.info(f"{self.name} is transferring from email write to email read")
                self.current_state = self.email_read
            elif char >= 1 - np.sum(self.trans_matrix[:8, 7]):
                logging.info(f"{self.name} stays in email write")
                self.current_state = self.email_write
            else:
                break

    @prime
    def _create_mock_location(self):
        """
        Creates the "mock location" state of the machine.

        Modifies the GPS location and then logs it via Google Maps.

        :return: Nothing
        """
        while True:
            char = yield
            # True, if it's weekend
            if is_weekend():
                # True, if it's time for weekend activity
                if weekend(self.person):
                    latitude = self.weekend_activity_location['latitude']
                    longitude = self.weekend_activity_location['longitude']
                # True, if it's time to go home
                else:
                    latitude = self.home_location['latitude']
                    longitude = self.home_location['longitude']
            # True, if it's work time
            elif is_working(self.person):
                latitude = self.work_location['latitude']
                longitude = self.work_location['longitude']
            # True, if it's after work time
            elif is_enjoying(self.person):
                latitude = self.spare_time_location['latitude']
                longitude = self.spare_time_location['longitude']
            # True, if it's time to go home
            else:
                latitude = self.home_location['latitude']
                longitude = self.home_location['longitude']
            self.location_spoofer(self.device, latitude, longitude)

            if char >= 1 - np.sum(self.trans_matrix[:9, 8]):
                logging.info(f"{self.name} is transferring from mock location to idle")
                self.current_state = self.idle
            else:
                break

    @prime
    def _create_browse(self):
        """
        Creates the "browse" state of the machine.

        Populates the browsing history for Google Chrome.

        :return: Nothing
        """
        while True:
            char = yield
            filepath = os.path.join(ROOT_DIR, 'datasets', 'browser_history', self.token)
            # Visit some random websites from list
            populate_random(filepath, self.device, 1)

            if char >= 1 - np.sum(self.trans_matrix[:10, 9]):
                logging.info(f"{self.name} is transferring from browse to idle")
                self.current_state = self.idle
            else:
                break

    def get_open_conv_partners(self) -> List[str]:
        """
        Creates a list of all the people that can be chatted with and currently don't have an open conversation.

        :return: list of people (token) strings
        """
        list_of_partners = []
        for con in open_conv:
            # filter out the group chats
            if 'previous message' in con.columns:
                continue
            else:
                list_of_partners.extend(list(con['agent']))
        # return a list where each partner only appears once
        list_of_partners = list(set(list_of_partners))
        if self.token in list_of_partners:
            list_of_partners.remove(self.token)
        return list_of_partners

    def check_online(self) -> None:
        """
        Checks for the message right above the list of chats that occurs when the phone does not have an active internet
        connection.

        If the message is displayed the Persons status is set to not active, active else.

        The message is only displayed after interaction with whatsapp web such as sending a message.

        Other possible messages are for example: "Enable desktop notifications"

        Assumptions:
                        - the text indicating that the phone has no internet connection is: 'Phone not connected'
                        - the text indicating that the pc is not connected is: 'Computer not connected'
                        LANGUAGE SPECIFIC

        :return: Nothing
        """
        try:
            msgs = self.whatsapp.find_elements_by_xpath("//*[@class='_2z7gr']")
            if len(msgs) > 0:
                for msg in msgs:
                    if msg.text == 'Phone not connected':
                        if self.is_active:
                            logging.warning(
                                f'{self.name} ({self.token}) has no internet connection and is set to inactive')
                        self.is_active = False
                        break
                    if msg.text == 'Computer not connected':
                        logging.critical('The computer seems to have no internet connection')
                        if self.is_active:
                            logging.warning(f'{self.name} ({self.token}) is set to inactive')
                        self.is_active = False
                        break
            else:
                if not self.is_active:
                    logging.info(f'{self.name} is set back to active')
                self.is_active = True
        except (NoSuchElementException, StaleElementReferenceException):
            print('Exception in check online')

    def select_chat(self, name: str, group: list = None) -> "WhatsappFSM":
        """
        Selects a chat from the list of chats.
        If chat doesn't exist yet, the chat is opened, provided the contact (=name) exists in the contacts of the phone.
        Is also able to open and create group chats.

        Assumptions:
                        - There is a button to start a new chat in the 'header'
                        - You can search for contacts and groups in the search field when starting a new chat
                        - If no chat is found, you can go back by clicking button '_18eKe'
                        - After a group chat is created, Whatsapp automatically opens the chat window

        :param self: Person object that should select the chat
        :param group: list of group members to be added
        :param name: name of the contact or group
        :return: Person
        """
        try:
            # try to open chat
            self.whatsapp.find_element_by_xpath(f"//*[@title='{name}']").click()
            self.last_contact = name
            logging.info(f'{self.name} selected chat with {name}')
        except NoSuchElementException:
            if not group:
                try:
                    # click on 'start new chat'
                    self.whatsapp.find_element_by_xpath('//*[@aria-label="New chat"]').click()
                    # search for chat
                    self.whatsapp.find_element_by_xpath(
                        '//*[@class="_13NKt copyable-text selectable-text"]').send_keys(name)
                    # click on chat
                    self.whatsapp.find_element_by_xpath(f"//*[@title='{name}']").click()
                    self.last_contact = name
                    logging.info(f'New chat with {name} opened')
                except NoSuchElementException:
                    logging.critical(f'{self.name} failed to open chat with {name}')
                    # click back button
                    self.whatsapp.find_element_by_xpath("//*[@class='_18eKe']").click()
            else:
                try:
                    # click on 'start new chat'
                    self.whatsapp.find_element_by_xpath('//*[@aria-label="New chat"]').click()
                    # click on 'New Group'
                    self.whatsapp.find_element_by_xpath('//*[@class="_2nY6U"]').click()
                    # add all group members
                    for member in group:
                        self.whatsapp.find_element_by_xpath(
                            '//*[@class="_1x9wV copyable-text selectable-text"]').send_keys(member)
                        path = f"//*[@title='{member}']"
                        try:
                            self.whatsapp.find_element_by_xpath(path).click()
                            logging.info(f'{member} added to group chat')
                        except NoSuchElementException:
                            self.whatsapp.find_element_by_xpath(
                                '//*[@class="_1x9wV copyable-text selectable-text"]').clear()
                            logging.warning(f'failed to add {member} to group chat')
                    time.sleep(1)
                    # click arrow forward button
                    self.whatsapp.find_element_by_xpath('//*[@class="_165_h"]').click()
                    # enter group name
                    self.whatsapp.find_element_by_xpath(
                        '//*[@class="_13NKt copyable-text selectable-text"]').send_keys(name)
                    # click finish
                    self.whatsapp.find_element_by_xpath('//*[@class="_165_h"]').click()
                    # wait for gui to load
                    time.sleep(2)
                    logging.info(f'Created Group chat with {group}')

                except NoSuchElementException:
                    logging.critical('Failed to create group chat')
                    try:
                        self.whatsapp.find_element_by_xpath("//*[@class='_18eKe']").click()
                        self.whatsapp.find_element_by_xpath("//*[@class='_18eKe']").click()
                        self.whatsapp.find_element_by_xpath("//*[@class='_18eKe']").click()
                    except NoSuchElementException:
                        pass
        except ElementClickInterceptedException:
            logging.warning('ElementClickInterceptedException occurred')
            return self.select_chat(name, group)
        return self

    def send_text(self, text: str) -> "WhatsappFSM":
        """
        Sends a message to the other contact.

        Assumptions:
                        - you are currently in a active chat window
                        - there is a text field
                        - pressing enter sends the message

        In order to be able to send Emojis the text is entered via JavaScript.

        The text can not have \" in it -> otherwise the javascript (+ python) would not work
        The function tries to deal with those cases by replacing \" with \'.

        Furthermore \n is replaced with '<br />' s.t. line breaks are displayed correctly.

        :param self: Person that sends the text
        :param text: text to be sent
        :return: Nothing
        """
        try:
            # replace values
            text = text.replace('\n', '<br />').replace('\"', '\'').strip('\n')
            input_box = self.whatsapp.find_elements_by_xpath('//*[@class="_13NKt copyable-text selectable-text"]')[-1]
            self.whatsapp.execute_script('arguments[0].innerHTML = "{}"'.format(text), input_box)
            input_box.send_keys('.')
            input_box.send_keys(Keys.BACKSPACE)
            time.sleep(len(text.split()) * self.typing_speed)
            input_box.send_keys(Keys.ENTER)
            logging.info(f'{self.name} sent message: {text}')
        except (JavascriptException, InvalidArgumentException):
            logging.warning(f"Message skipped: {text}")
        except ElementNotInteractableException:
            logging.warning('Element was not interactable, trying again')
            self.send_text(text)
        except Exception as e:
            logging.error(f"Message skipped: Exception {e} occurred")
        return self

    def send_voice_msg(self, text: str) -> "WhatsappFSM":
        """
        Sends the given text as a voice Message.

        Prerequisites:
                        - Sound output has to be rerouted to sound input

                        - We achieved this by connecting an external sound card and connecting one aux cable to input
                        and output

        :param text: text to be sent
        :return: self
        """
        try:
            msg = gTTS(text, lang='en')
            path_to_vm = os.path.join(self.token_dir, f"{self.token}_voice_msg.mp3")
            msg.save(path_to_vm)
            logging.info(f"voice msg stored to {path_to_vm}")
            logging.info(f"starting voice recording for {self.name}")
            self.whatsapp.find_element_by_xpath('//*[@class="_30ggS"]').click()
            playsound(path_to_vm)
            #_6I6m-
            self.whatsapp.find_elements_by_xpath('.//*[contains(@class, "_1BYAo")]')[-1].click()
            logging.info(f"{self.name} sent a voice message")
        except ElementNotInteractableException:
            try:
                logging.warning('Voice message could not be sent trying to send it again')
                self.whatsapp.find_elements_by_xpath('.//*[contains(@class, "_6I6m-")]')[-1].click()
            except ElementNotInteractableException:
                logging.critical('Voice message could not be sent trying to reload WhatsApp')
                self.whatsapp.refresh()
                self.whatsapp.wait.until(
                    ec.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[4]/div/div')))
        except Exception as e:
            logging.critical(f"Exception {e} occurred in send voice msg")
            traceback.print_exc()
        return self

    def send_attachment(self, attachment: str) -> "WhatsappFSM":
        """
        Sends an attachment in an active Whatsapp chat

        Assumptions:
                        - you are currently in an active chat window
                        - there is a paperclip icon in the 'footer'
                        - after you click the paperclip icon there is an element with the tag name 'input'
                        - you can insert the attachment via send_keys()
                        - after the attachment is inserted there is a send button

        Currently tested with .mp3, .mpeg .mp4, .pdf, .jpg, .jpeg and .png

        :param self: Person that should send the attachment
        :param attachment: path to attachment
        :return: Person
        """
        try:
            # Click on paperclip icon
            self.whatsapp.find_element_by_xpath('//*[@id="main"]/footer/div[1]/div[1]/span[2]/div[1]/div[1]/div[2]').click()
            # give gui time
            time.sleep(1)
            input_box = self.whatsapp.find_element_by_tag_name('input')
            # insert picture
            input_box.send_keys(attachment)
            # give gui time
            time.sleep(1)
            # click send
            self.whatsapp.find_element_by_xpath(
                '//*[@id="app"]/div/div/div[2]/div[2]/span/div/span/div/div/div[2]/div/div[2]/div[2]/div/div/span')\
                .click()
            logging.info(f'Attachment {attachment} sent')
            time.sleep(2)
        except NoSuchElementException:
            logging.warning(f'Failed to send {attachment}')
            self.whatsapp.find_element_by_xpath("//*[@class='_18eKe']").click()
        return self

    def reply_to_text(self, message_to_reply_to: str) -> "WhatsappFSM":
        """
        Tries to reply to the specified message in an active chat window

        Assumptions:
                        - you are currently in an active chat window

        The function tries find the text of the last message on the screen.
            -> if it is not found, the function fails

        :param self: Person that tries to reply to a message
        :param message_to_reply_to: text of the message that should be replied to
        :return: Nothing
        """
        try:
            time.sleep(len(message_to_reply_to.split()) * self.typing_speed)
            message = self.whatsapp.find_element_by_xpath(f"//*[contains(text(), '{message_to_reply_to}')]")
            hover = ActionChains(self.whatsapp).move_to_element(message)
            hover.perform()
            # self.whatsapp.find_element_by_xpath("//*[contains(@class,'_3Y9uf') or contains(@class,'QhSbI')]").click()
            self.whatsapp.find_element_by_xpath("//*[@class='_3e9My']").click()
            self.whatsapp.find_element_by_xpath("//*[contains(text(), 'Reply')]").click()
            logging.info(f'Replying to message <{message_to_reply_to}>')
        except NoSuchElementException:
            logging.warning(f'Message <{message_to_reply_to}> could not be found')
        except MoveTargetOutOfBoundsException:
            logging.warning(f'Message <{message_to_reply_to}> is out of range')
        except Exception as e:
            logging.warning(f'Replying to <{message_to_reply_to}> failed')
            logging.error(f'Exception {e} occurred')
        return self

    def read_green_dot(self):
        """
        Searches for a green dot, that signals, that a message has been received, in the list of conversations.
        If such a green dot is found the number (= n) in it is extracted.
        Then the chat is clicked and the last n messages are extracted.
        Then the person takes the time to read the messages (time.sleep).

        Assumptions:
                        - There is a Number in the dot
                            -> the "green dot" can also be created with "mark as unread", but then there is no number in
                            it as far as I know
                            -> the program assumes that this is not the case

        :return: Nothing
        """
        try:
            chat = self.whatsapp.find_element_by_xpath('//*[@class="_23LrM"]')
            msg = chat.get_attribute("aria-label")
            chat.click()
            nmbr = int(msg.split()[0])
            sender = self.whatsapp.find_elements_by_xpath('.//*[contains(@class, "message-in")]')[-nmbr:]
            nmbr_of_words = 0
            for msg in sender:
                nmbr_of_words += len(msg.text.split()[:-1])
            time.sleep(nmbr_of_words * self.reading_speed)
        except NoSuchElementException:
            return self
        except Exception:
            traceback.print_exc()
            return self
        return self

    def get_conv(self, data_frame: pd.DataFrame, key: str, conv_partner: "WhatsappFSM") -> pd.DataFrame:
        """
        Fetches a conversation from the amazon json and formats the data for our purposes.

        Assumptions:
                        - The dataframe (df) is formatted like the amazon conversational dataset json
                            -> df.get(key) -> another dataframe with column 'content'
                            -> df.get(key).get('content') -> the conversation with columns 'agent' and 'message'
                            - agents are either 'agent_1' or 'agent_2'
                                -> agent_1 always begins the conversation

        :param data_frame: conversational data
        :param key: key of the data_frame
        :param conv_partner: Person that is the conversation partner
        :return: formatted data
        """
        possible_conversations.remove(key)
        data = pd.DataFrame(data_frame.get(key).get('content'))
        data = data.replace("agent_1", self.token)
        data = data.replace("agent_2", conv_partner.token)
        data = data[['message', 'agent']]
        data['chatname'] = data.apply(
            lambda row: self.name if row.agent == conv_partner.token else conv_partner.name, axis=1)
        return data

    def get_group_conv(self, data_frame: pd.DataFrame, key: str,
                       other_group_members: List[str], number: int) -> pd.DataFrame:
        """
        Fetches a conversation from the reddit json that is produced by 'reddit_comments.py'
        and formats the data for our purposes.

        Assumptions:
                        - The dataframe (df) is formatted similar to the amazon conversational dataset json
                            -> df.get(key) -> another dataframe with column 'content'
                            -> df.get(key).get('content') -> list(list(one dataframe))
                                -> the dataframe has columns: 'author', 'body' and 'previous message'

        The function calls the get_group_chat function that returns an anonymized and shortened version of the generated
        DataFrame

        :param data_frame: conversational data from reddit
        :param key: key of the data_frame
        :param other_group_members: list[Person] that should be the other participants of the conversation
                                    - if the group is created with this conversation these are all the members of the
                                    group
        :param number: number of chat
        :return: anonymized DataFrame
        """
        possible_group_conversations[number].remove(key)
        data = data_frame.get(key).get('content')
        liste = []
        for dat in data:
            liste.append(pd.DataFrame(dat))
        return self.get_group_chat(other_group_members, liste)

    def get_group_chat(self, other_people: List[str], conversation: List[pd.DataFrame]) -> pd.DataFrame:
        """
        Assigns to each reddit username a Person.

        Assumptions:    - conversation is a list that contains one or multiple DataFrames
                            -> the first element in this list is the initial post
                            -> if present, all the other DataFrames in the list are answer threads to the initial post

        The function first connects the first n (= number of group members) entries in the list to one big DataFrame.
        Then the initiator is assigned to the original poster.
        Then while there is still a reddit username that is not yet overridden:
            - a random member of (other_people - last Person that was chosen - initiator) is assigned to the next
            username that is not yet anonymized.

        At last the columns are renamed to match the columns of the anonymized amazon conversation.

        :param other_people: list[Person] that will be the other participants of the conversation
                             - if the group is created with this conversation these are all the members of the group
        :param conversation: list of DataFrames
        :return: anonymized conversation
        """
        all_people = other_people[:]
        all_people.append(self.token)
        conversation = conversation[:len(all_people)]
        conversation = pd.concat(conversation, ignore_index=True)
        conversation['author'] = conversation.replace(conversation['author'].iloc[0], self.token)
        last_contact = self.token
        # solange noch mindestens ein alias noch nicht überschrieben wurde
        while not conversation[~conversation.author.isin(all_people)].empty:
            random_member = random.choice([p for p in other_people if p != last_contact])
            conversation['author'] = conversation.replace(conversation[~conversation.author.isin(all_people)].iloc[0],
                                                          random_member)
            last_contact = random_member
        # make column names match those from amazon
        conversation.rename({'body': 'message', 'author': 'agent'}, axis=1, inplace=True)
        return conversation

    def begin_new_conversation(self, conv_partner: "WhatsappFSM") -> pd.DataFrame:
        """
        Sends the first message of a random conversation of the amazon dataset.

        The key is removed from the list of possible conversations.
        The first line of the DataFrame of the conversation gets deleted.
        The conversation is added to the list of open conversations.

        :param conv_partner: Person that is written to
        :return: DataFrame of the remaining conversation
        """
        conversation_id = random.choice(possible_conversations)
        logging.info(f"starting new conversation - key: {conversation_id}")
        conversation = self.get_conv(one_on_one_conv, conversation_id, conv_partner)
        self.select_chat(conversation['chatname'].iloc[0])
        vm_prob = random.uniform(0, 1)
        if vm_prob > self.voice_message_probability:
            self.send_text(conversation['message'].iloc[0])
        else:
            self.send_voice_msg(conversation['message'].iloc[0])
        conversation.drop(conversation.index[0], inplace=True)
        open_conv.append(conversation)
        return conversation

    def begin_new_group_conversations(self, group_chat: tuple, number: int):
        """
        Sends the first message of a random conversation of the reddit group conversations dataset.

        The key is removed from the list of possible group conversations.
        The first line of the DataFrame of the conversation gets deleted.
        The conversation is added to the list of open conversations.

        :param group_chat: group chat tuple
        :param number: number of chat
        :return: conversation
        """
        chatname = group_chat[0]
        members = group_chat[1]
        conversation_id = random.choice(possible_group_conversations[number])
        initiator = self.token
        other_people = [p for p in members if p != initiator]
        logging.info(f"starting new conversation in group {chatname} - key: {conversation_id}")
        conversation = self.get_group_conv(group_chats[number], conversation_id, other_people, number)
        conversation['chatname'] = chatname
        self.select_chat(chatname, [o.name for o in objects if o.token in other_people])
        self.send_text(conversation['message'].iloc[0])
        conversation.drop(conversation.index[0], inplace=True)
        if not conversation.empty:
            open_conv.append(conversation)
        return conversation

    def read_conversation(self, conversation: pd.DataFrame) -> "WhatsappFSM":
        """
        Marks the given conversation as read.

        :param conversation: conversation that should be read
        :return: WhatsappFSM object
        """
        if not self.is_active:
            return self
        self.select_chat(conversation['chatname'].iloc[0])
        time.sleep(5)
        return self

    def continue_conversation(self, conversation: pd.DataFrame) -> "WhatsappFSM":
        """
        Continues the given conversation.

        Assumptions:
                    - The conversation is from the list of open conversations
                        -> all the DataFrames in this list are almost formatted the same ('previous message' in group
                        chats)
                                -> columns: 'agent', 'message', 'chatname' (, 'previous message')

        :param conversation: conversation that should be continued
        :return: Person
        """
        if not self.is_active:
            return self
        self.select_chat(conversation['chatname'].iloc[0])
        if 'previous message' in conversation.columns:
            self.reply_to_text(conversation['previous message'].iloc[0])
        vm_prob = random.uniform(0, 1)
        if vm_prob > self.voice_message_probability:
            self.send_text(conversation['message'].iloc[0])
        else:
            self.send_voice_msg(conversation['message'].iloc[0])
        attach_prob = random.uniform(0, 1)
        if attach_prob < self.attachment_probability:
            path = os.path.join(ROOT_DIR, 'datasets', 'pictures', 'without_meta')
            picture = random.choice(os.listdir(path))
            self.send_attachment(path + '/' + picture)
        conversation.drop(conversation.index[0], inplace=True)
        if conversation.empty:
            del conversation
        return self

    def location_spoofer(self, dev: Device, lat, long):
        """
        Start or stop the location spoofing app, called Appium Settings

        :param dev: connected device
        :param lat: latitude of the place
        :param long: longitude of the place
        :return: Nothing
        """
        # Open app
        dev.shell('monkey -p io.appium.settings 1')
        # Changing location for newer android versions
        dev.shell('am start-foreground-service --user 0 -n io.appium.settings/.LocationService '
                    f'--es longitude {str(long)} '
                    f'--es latitude {str(lat)}')
        # Changing location for older android versions
        dev.shell('am startservice --user 0 -n io.appium.settings/.LocationService '
                    f'--es longitude {str(long)} '
                    f'--es latitude {str(lat)}')
        # Opens Google Maps to log the location
        dev.shell('monkey -p com.google.android.apps.maps 1')
        print(f'Location spoofing activated on {dev.serial}.')
        print(f'Device is located at latitude: {lat} and longitude: {long}')
        time.sleep(15)
