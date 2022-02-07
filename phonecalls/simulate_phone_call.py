"""
Module to simulate a phone call between two phones
"""
import logging
import time
import random

import ppadb.device


def simulate_phone_call(caller: ppadb.device.Device, callee: object, callee_number: str, duration: float) -> None:
    """
    Simulates a phone call between two phones

    Assumptions:
        - Both phones have usb debugging enabled and are connected to the pc
        - Both devices are unlocked

    :param caller: phone that calls
    :param callee: phone that is called
    :param callee_number: phone number of the callees phone
    :param duration: duration of the call
    :return: Nothing
    """
    # call the callee
    caller.shell(f'am start -a android.intent.action.CALL -d tel:{callee_number}')
    logging.info(f'{caller} tries to call {callee}')
    # give time to answer phone
    time.sleep(10)
    # pick up call
    callee.shell('input keyevent KEYCODE_CALL')
    # sleep for duration of the call
    time.sleep(duration)
    # random person hangs up
    random.choice([caller, callee]).shell('input keyevent KEYCODE_ENDCALL')
    # give gui some time
    time.sleep(2)
    caller.shell('input keyevent KEYCODE_HOME')
    logging.info(f'{caller} returned to home screen')
    callee.shell('input keyevent KEYCODE_HOME')
    logging.info(f'{callee} returned to home screen')
