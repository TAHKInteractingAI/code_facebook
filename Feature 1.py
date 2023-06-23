from copy import copy
from tabnanny import check
import time
import csv
from unittest import skip
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import pytz
import selenium
import configparser
import argparse
import os
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from termcolor import colored
from selenium.webdriver.common.by import \
    By  # https://stackoverflow.com/questions/69875125/find-element-by-commands-are-deprecated-in-selenium
import random
import numpy as np
from selenium.webdriver.common.proxy import *
from selenium import webdriver
import random
from selenium.webdriver.common.proxy import Proxy, ProxyType

print("Current selenium version is:", selenium.__version__)
# Select webdriver profile to use in selenium or not.
import sys
import os
import undetected_chromedriver as uc
import time

def driver_Profile(Profile_name):
    if Profile_name == "Yes":
        ### Selenium Web Driver Chrome Profile in Python
        # set proxy and other prefs.
        profile = webdriver.FirefoxProfile()
        profile.set_preference("network.proxy.type", 1)
        profile.set_preference("network.proxy.http", allproxs[0]['IP Address'])
        profile.set_preference("network.proxy.http_port", int(allproxs[0]['Port']))
        # update to profile. you can do it repeated. FF driver will take it.
        profile.set_preference("network.proxy.ssl", allproxs[0]['IP Address']);
        profile.set_preference("network.proxy.ssl_port", int(allproxs[0]['Port']))
        # profile.update_preferences()
        # You would also like to block flash
        # profile.set_preference('dom.ipc.plugins.enabled.libflashplayer.so', False)
        profile.set_preference("media.peerconnection.enabled", False)

        # save to FF profile
        profile.update_preferences()
        driver = webdriver.Firefox(profile, executable_path='./geckodriver')
        # webrtcshield = r'/home/qtdata/PycharmProjects/BotSAM/webrtc_leak_shield-1.0.7.xpi'
        # driver.install_addon(webrtcshield)
        # urbanvpn = r'/home/qtdata/PycharmProjects/BotSAM/urban_vpn-3.9.0.xpi'
        # driver.install_addon(urbanvpn)
        # driver.profile.add_extension(webrtcshield)
        # driver.profile.add_extension(urbanvpn)
        # driver.profile.set_preference("security.fileuri.strict_origin_policy", False)
        ### Check the version of Selenium currently installed, from Python
        print("Current selenium version is:", selenium.__version__)
        print("Current web browser is", driver.name)
        ### Current time using time module
        ## current_time = time.strftime("%H:%M:%S", time.localtime())
        ## print("Current time is:",current_time)
        ### datetime object containing current date and time
        now = datetime.now()
        ### dd/mm/YY H:M:S
        dt_string = now.strftime("%B %d, %Y    %H:%M:%S")
        print("Current date & time is:", dt_string)
        print(colored("You are using webdriver profile!", "red"))
    else:
        driver = uc.Chrome(executable_path=r'/home/qtdata/PycharmProjects/BotSAM/chromedriver')
        ### Check the version of Selenium currently installed, from Python
        print("Current selenium version is:", selenium.__version__)
        print("Current web browser is", driver.name)
        ### Current time using time module
        ## current_time = time.strftime("%H:%M:%S", time.localtime())
        ## print("Current time is:",current_time)
        ### datetime object containing current date and time
        now = datetime.now()
        ### dd/mm/YY H:M:S
        dt_string = now.strftime("%B %d, %Y    %H:%M:%S")
        print("Current date & time is:", dt_string)
        print(colored("You are NOT using webdriver profile!", "red"))
    return driver

def Login_Facebook():
    baseDir = os.path.dirname(os.path.realpath(sys.argv[0])) + os.path.sep
    """ Setup Argument Parameters """
    config = configparser.RawConfigParser()
    config.read(baseDir + 'Facebook Account.cfg')
    api_key = config.get('API_KEYS', 'hunter')
    username = config.get('CREDS', 'facebook_username')
    password = config.get('CREDS', 'facebook_password')
    # head to Facebook login page
    driver.get("https://www.facebook.com/login")
    time.sleep(3)
    # find username/email field and send the username itself to the input field
    driver.find_element(By.ID, "email").send_keys(username)
    # find password input field and insert password as well
    driver.find_element(By.ID, "pass").send_keys(password)
    # click login button
    driver.find_element(By.ID, "loginbutton").click()
    # wait the ready state to be complete & get the errors (if there are)
    time.sleep(5)
    errors = driver.find_elements(By.CLASS_NAME, "form__label--error ")
    # print the errors optionally
    for e in errors:
        print("errors massage: ", e.text)
    # if we find that error message within errors, then login is failed
    if driver.current_url == "https://www.facebook.com/":
        print(colored("Login Facebook successful!", "blue"))
        return True
    else:
        print(colored("Login Facebook failed!", "red"))
        return False

def Scroll_Pages_infinite_loading ():
    ### Scroll to a page with infinite loading, like social network ones, facebook etc.
    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    print("Begin scroll to a page with infinite loading.")
    # print("Begin Document Height", last_height)
    y = 0
    while True:
        # Scroll down to bottom
        for timer in range(0, 100):
            driver.execute_script("window.scrollTo(0, " + str(y) + ")")
            y += random.choice(np.arange(50, 60, 1)) # increase height random
            # print(random.choice(np.arange(50, 60, 1)), "&", y)
            time.sleep(0.1)
        # Wait to load page
        time.sleep(round(random.choice(np.arange(2, 5, 0.1)), 1))  # time sleep random
        # print("time sleep", round(random.choice(np.arange(2, 5, 0.1)), 1))
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print("Stop scroll page with infinite loading.")
            break
        else:
            # print("new height", new_height, "last height", last_height)
            last_height = new_height

def get_groups():
    links = {}
    with open('keywords.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            keyword = ''.join(row)
            driver.get('https://www.facebook.com/search/groups/?q=' + keyword)
            time.sleep(2)
            Scroll_Pages_infinite_loading()
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            for website in soup.findAll('a', class_='oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gpro0wi8 oo9gr5id lrazzd5p', href=True):
                links[website.get_text(strip=True)] = website['href']
            time.sleep(2)
            facebook_groups = pd.DataFrame(list(links.items()), columns=['Name', 'Website'])
            facebook_groups.to_csv(f'{keyword}_facebook_groups.csv', index=False)

if __name__ == '__main__':
    ### Select using drive profile or not ("Yes" or "No")
    ### Get time of a Python program's execution
    start_time = datetime.now()
    driver = driver_Profile('No')

    # linkedin groups
    results = Login_Facebook()
    if results == True:
        links = get_groups()

    time.sleep(1)

    driver.quit()
    ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ### Get time of a Python program's execution
    ## start_time = datetime.now()
    ## do your work here
    end_time = datetime.now()
    print(colored('Duration time: {} seconds '.format(end_time - start_time), "blue"), "\n start_time:", start_time,
          "\n", "end_time  :", end_time)