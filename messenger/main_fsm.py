"""
Main branch of the modular fsm.
"""
import json
import logging
import random
import threading
import time
import traceback
import sys
import numpy as np

from datetime import datetime, timedelta
from messenger.whatsapp.modular_fsm_test.whatsapp_fsm import WhatsappFSM
from transitions import get_transitions
from definitions import open_emails
from ppadb.client import Client
from definitions import CONFIG_PATH
from definitions import open_conversations as open_conv, possible_conversations, possible_group_conversations, \
    possible_email_conversations


logging.basicConfig(
    level=logging.INFO,
    format='[%(asctime)s] %(filename)s:%(funcName)s() %(levelname)s - %(message)s',
    datefmt='%d.%m.%y %H:%M %Z'
)


# Connects to the Android devices
adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    sys.exit()


def prime(fun):
    """
    Used as an decorator in order to make the functions reach the yield statement and thus initiate the states.

    :param fun: function to be primed
    :return: Nothing
    """

    def wrapper(*args, **kwargs):
        v = fun(*args, **kwargs)
        v.send(None)
        return v

    return wrapper


class Person:

    def __init__(self, person_details, transitions, **kwargs):

        self.transitions = np.array(transitions)
        self.idle = self._create_idle()
        self.name = person_details['First name'] + " " + person_details['Surname']
        self.active_hours = person_details['Mobile devices'][0]['active times']
        self.is_active = False
        self.kwargs = kwargs
        self.__dict__.update(kwargs)
        self.last_branch = self
        self.current_state = self.idle
        self.stopped = False

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
        Creates the idle state for the machine.
        Checks whether the person should be active or not, based on the active_hours of the person object.

        :return: Nothing
        """
        while True:
            char = yield
            in_time = False
            date = datetime.now().strftime('%Y-%d-%m')
            for key, value in self.active_hours.items():
                lower = datetime.strptime(date + " " + key, '%Y-%d-%m %H:%M')
                upper = lower + timedelta(minutes=int(value))
                if lower < datetime.now() < upper:
                    in_time = True
                    break
            if in_time:
                if not self.is_active:
                    logging.info(f"{self.name} is now active")
                self.is_active = True
            else:
                if self.is_active:
                    logging.info(f"{self.name} is now inactive")
                self.is_active = False
            if self.is_active:
                for j, kwarg in enumerate(self.kwargs.items()):
                    if char > 1 - np.sum(self.transitions[:j+1]):
                        logging.info(f"{self.name} is transferring from start to {kwarg[0]}")
                        self.current_state = self.kwargs[kwarg[0]].get_idle(self)
                        self.last_branch = self.kwargs[kwarg[0]]
                        break
            else:
                logging.info(f"{self.name} is inactive")
                time.sleep(600)


# Start of the WhatsApp chat bot
def start(fsm: Person, placeholder=None) -> None:
    try:
        while True:
            random_number = random.uniform(0, 1)
            if fsm.current_state is not fsm.idle:
                fsm.last_branch.send(random_number)
            else:
                fsm.send(random_number)
            if fsm.last_branch.current_state is fsm:
                fsm.current_state = fsm.idle
            time.sleep(1)
    except:
        traceback.print_exc()


with open(CONFIG_PATH, 'r') as f:
    config = json.load(f)

dev = []
for i, d in enumerate(devices):
    device = devices[i]
    for j in range(len(config['People'])):
        if config['People'][j]['Mobile devices'][0]['Serial number'] == device.serial:
            dev.append(device)

# Setting up the participants of the WhatsApp chats
trans_a = get_transitions(config['People'][0]['Mobile devices'][0]['Whatsapp token'])
a = Person(config['People'][0], trans_a, whatsapp=WhatsappFSM(config['People'][0], dev[0], trans_a))

trans_b = get_transitions(config['People'][1]['Mobile devices'][0]['Whatsapp token'])
b = Person(config['People'][1], trans_b, whatsapp=WhatsappFSM(config['People'][1], dev[1], trans_b))

trans_c = get_transitions(config['People'][2]['Mobile devices'][0]['Whatsapp token'])
c = Person(config['People'][2], trans_c, whatsapp=WhatsappFSM(config['People'][2], dev[2], trans_c))

trans_d = get_transitions(config['People'][3]['Mobile devices'][0]['Whatsapp token'])
d = Person(config['People'][3], trans_d, whatsapp=WhatsappFSM(config['People'][3], dev[3], trans_d))

trans_e = get_transitions(config['People'][4]['Mobile devices'][0]['Whatsapp token'])
e = Person(config['People'][4], trans_e, whatsapp=WhatsappFSM(config['People'][4], dev[4], trans_e))

threads = []
try:
    pa = threading.Thread(target=start, args=(a, config['People'][0]))
    threads.append(pa)
    pb = threading.Thread(target=start, args=(b, config['People'][1]))
    threads.append(pb)
    pc = threading.Thread(target=start, args=(c, config['People'][2]))
    threads.append(pc)
    pd = threading.Thread(target=start, args=(d, config['People'][3]))
    threads.append(pd)
    pe = threading.Thread(target=start, args=(e, config['People'][4]))
    threads.append(pe)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
except Exception as e:
    traceback.print_exc()
    try:
        for thread in threads:
            thread.join()
    except Exception as e:
        traceback.print_exc()
finally:
    for i, conv in enumerate(open_conv):
        open_conv[i] = conv.to_dict(orient='records')
    for i, mail in enumerate(open_emails):
        open_emails[i] = mail.to_dict(orient='records')

    state_data = {
        'conversations': open_conv,
        'email conversations': open_emails,
        'possible chats': possible_conversations,
        'possible group chats': possible_group_conversations,
        'possible emails': possible_email_conversations
    }
    logging.info('Saving conversations for next run')
    with open('conversations.json', 'w+') as f:
        json.dump(state_data, f)
