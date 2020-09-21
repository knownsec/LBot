#!/usr/bin/env python
# encoding: utf-8
'''
@author: LoRexxar
@contact: lorexxar@gmail.com
@file: chromeheadless.py.py
@time: 2020/3/17 15:17
@desc:
'''


import time

import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

import os
import traceback
from urllib.parse import urlparse

from LBot.settings import CHROME_WEBDRIVER_PATH, HOME_PAGE
from utils.base import random_string
from utils.log import logger


class ChromeDriver:
    def __init__(self):
        self.chromedriver_path = CHROME_WEBDRIVER_PATH
        self.checkos()

        try:
            self.init_object()

        except selenium.common.exceptions.SessionNotCreatedException:
            logger.error("[Chrome Headless] ChromeDriver version wrong error.")
            exit(0)

        except selenium.common.exceptions.WebDriverException:
            logger.error("[Chrome Headless] ChromeDriver load error.")
            exit(0)

        self.origin_url = ""

    def checkos(self):

        if os.name == 'nt':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_win32.exe")
        elif os.name == 'posix':
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_linux64")
        else:
            self.chromedriver_path = os.path.join(self.chromedriver_path, "chromedriver_mac64")

    def init_object(self):

        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument('--headless')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-images')
        self.chrome_options.add_argument('--ignore-certificate-errors')
        self.chrome_options.add_argument('--allow-running-insecure-content')
        # self.chrome_options.add_argument('blink-settings=imagesEnabled=false')
        self.chrome_options.add_argument('--omnibox-popup-count="5"')
        self.chrome_options.add_argument("--disable-popup-blocking")
        self.chrome_options.add_argument("--disable-web-security")
        self.chrome_options.add_argument("--disk-cache-size=1000")

        prefs = {'profile.default_content_settings.popups': 0, 'download.default_directory': '/tmp'}
        self.chrome_options.add_experimental_option('prefs', prefs)

        self.chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')

        self.driver = webdriver.Chrome(chrome_options=self.chrome_options, executable_path=self.chromedriver_path)

        self.driver.set_page_load_timeout(15)
        self.driver.set_script_timeout(5)

    def get_resp(self, url, cookies=None, times=0):

        try:
            self.driver.implicitly_wait(10)
            self.driver.get(HOME_PAGE)

            if cookies:
                self.add_cookie(cookies)
                self.driver.implicitly_wait(10)
                self.driver.get(url)

            time.sleep(3)

            self.driver.switch_to.alert.accept()

            return self.driver.page_source

        except selenium.common.exceptions.NoAlertPresentException:
            return False

        except selenium.common.exceptions.InvalidSessionIdException:
            logger.warning("[ChromeHeadless]Chrome Headless quit unexpectedly..")

            self.init_object()

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, cookies, times + 1)
            return False

        except selenium.common.exceptions.TimeoutException:
            logger.warning("[ChromeHeadless]Chrome Headless request timeout..{}".format(url))
            if times > 0:
                return False

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, cookies, times+1)
            return False

        except selenium.common.exceptions.InvalidCookieDomainException:
            logger.warning("[ChromeHeadless]Chrome Headless request with cookie error..{}".format(url))

            logger.warning("[ChromeHeadless]retry once..{}".format(url))
            self.get_resp(url, None, times + 1)
            return False

        except selenium.common.exceptions.InvalidArgumentException:
            logger.warning("[ChromeHeadless]Request error...{}".format(url))
            logger.warning("[ChromeHeadless]{}".format(traceback.format_exc()))
            return False

    def add_cookie(self, cookies):

        for cookie in cookies.split(';'):
            key = cookie.split('=')[0].strip()
            value = cookie.split('=')[1].strip()

            if key and value:
                try:
                    self.driver.add_cookie({'name': key, 'value': value, 'httpOnly': True, 'HostOnly': True})

                except selenium.common.exceptions.UnableToSetCookieException:
                    logger.warning("[ChromeHeadless] Wrong Cookie {} set..".format(key))
                    continue

    def close_driver(self):
        self.driver.quit()
        # self.driver.close()
        time.sleep(1)

    def __del__(self):
        self.close_driver()
