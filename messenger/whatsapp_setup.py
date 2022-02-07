"""
Module to set up a Whatsapp session in Google Chrome
"""

import os
import logging
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from definitions import ROOT_DIR


FILE_DIR = os.path.dirname(os.path.abspath(__file__))


def whatsapp_setup(user: str, incognito=False, headless=False) -> webdriver:
    """
    Opens a Google Chrome window and opens Whatsapp web.

    Driver waits for the big picture right next to the chats to show up. (up to a minute)
    If this is the first time logging into Whatsapp the user must scan the QR code in order to log in.

    After the first time the cookies are stored and the user does not have to log in again
        - except the user is logged out, the cookies are deleted or the phone is switched (must be manually deleted)

    :param user: user whose cookies should be stored/ loaded
    :param incognito: should the session be an incognito session (-> no cookies are loaded/stored!)
    :param headless: should the session be a headless session (Google Chrome is running but no window is opened)
                    --> cookies must be stored already!
    :return: driver object
    """
    options = Options()
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("detach", True)
    options.add_experimental_option("useAutomationExtension", False)
    options.add_argument("--mute-audio")

    if incognito:
        options.add_argument("--incognito")
        logging.info('Driver is incognito - no user_data is loaded')
    else:
        user_dir = os.path.join(ROOT_DIR, 'Token', user, user)
        options.add_argument(f"user-data-dir={user_dir}")
        logging.info(f'user_data: {user_dir} loaded')
    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) '
                             'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36')
        logging.info('Driver is a headless driver')

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
    logging.info('Driver creation finished')

    driver.get("https://web.whatsapp.com")
    delay = 120
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div[1]/div[1]/div[4]/div/div')))
        logging.info("Whatsapp loaded")
    except TimeoutException:
        logging.critical("Loading Whatsapp web took too much time!")
    return driver
