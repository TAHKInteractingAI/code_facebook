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

def get_edited(keyword):
    # from csv, check if group is already in requested or joined
    driver.get('https://www.facebook.com/profile.php?sk=groups')
    # Check for each joined group is in csv files
    groups = driver.find_elements_by_class_name("d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em mdeji52x a5q79mjw g1cxx5fr lrazzd5p oo9gr5id")
    # Make a copy of the keyword csv
    filename = f'{keyword}_facebook_groups.csv'
    dfcopy = pd.read_csv(filename)
    for group in groups:
        if group in dfcopy:
            dfcopy.drop(group)
    dfcopy.to_csv('edited_' + filename)

def join_group(keyword):
    df = pd.read_csv(f'edited_{keyword}_facebook_groups.csv', usecols=['Name', 'Website'])
    websites = df['Website']
    i = 0
    while check_status() < 6000:
        url = websites[i]
        driver.get(url)
        time.sleep(5)
        if len(driver.find_elements_by_css_selector('[aria-label="Join Group"]')) > 0:
            driver.find_element_by_css_selector('[aria-label="Join Group"]').click()
            time.sleep(3)
            if len(driver.find_elements_by_xpath("//div[contains(@class, 'd2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 ns63r2gh iv3no6db o3w64lxj b2s5l15y hnhda86s oo9gr5id')]")) == 1:
                print('Hit request quota for today')
                break
        i +=1
    #check for current status
    if check_status() == 6000:
        print('Maximum number of groups joined (6000)')

def check_status():
    # go to groups page
    time.sleep(3)
    driver.get('https://www.facebook.com/profile.php?sk=groups')
    time.sleep(5)
    status = []
    # check the public groups page (might need to add private in future)
    num_of_joined = len(driver.find_elements_by_xpath("//a[contains(@class, 'oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8')]"))
    time.sleep(3)
    status = num_of_joined
    return status

def get_result():
    allstatus = {'Name': [], 'Facebook group': [], 'Result': []}
    # go to groups page for joined
    driver.get('https://www.facebook.com/profile.php?sk=groups')
    time.sleep(3)
    num_joined = len(driver.find_elements_by_class_name("oajrlxb2 g5ia77u1 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 nc684nl6 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x jb3vyjys rz4wbd8a qt6c0cv9 a8nywdso i1ao9s8h esuyzwwr f1sip0of lzcic4wl gmql0nx0 gpro0wi8"))
    for i in range(1, num_joined):
        link = driver.find_element_by_xpath(f'/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div/div/div[4]/div/div/div/div[1]/div/div/div/div/div[3]/div[{i}]]/div[2]/div[1]/a').get_attribute('href')
        driver.get(link)
        time.sleep(5)
        name = driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[3]/div/div/div[1]/div[1]/div[1]/div[2]/div/div/div/div/div[1]/div/div/div/div/div/div[1]/h1/span/a")
        allstatus['Name'].append(name.text)
        allstatus['Facebook group'].append(link)
        allstatus['Result'].append('Joined')

    # update status for the rest of the groups
    with open('keywords.csv', 'r') as csvfile:
        datareader = csv.reader(csvfile)
        for row in datareader:
            keyword = ''.join(row)
            df = pd.read_csv(f'{keyword}_facebook_groups.csv')
            row_count = df.shape[0]
            for i in range(1, row_count):
                if df['Name'][i] not in allstatus['Name']:
                    allstatus['Name'].append(df['Name'][i])
                    allstatus['Facebook group'].append(df['Website'][i])
                    allstatus['Result'].append('Limit request to join')
    print(allstatus['Name'])
    print(allstatus['Facebook group'])
    print(allstatus['Result'])
    allstatus = pd.DataFrame(allstatus)
    allstatus.to_csv('Facebook results.csv')

if __name__ == '__main__':
    ### Select using drive profile or not ("Yes" or "No")
    ### Get time of a Python program's execution
    start_time = datetime.now()
    driver = driver_Profile('No')

    # linkedin groups
    results = Login_Facebook()
    if results == True:
        with open('keywords.csv', 'r') as csvfile:
            datareader = csv.reader(csvfile)
            for row in datareader:
                keyword = ''.join(row)
                get_edited(keyword)
                # Join and post in LinkedIn group
                join_group(keyword)
        get_result()  # returns the date joined

    time.sleep(1)

    driver.quit()
    ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ### Get time of a Python program's execution
    ## start_time = datetime.now()
    ## do your work here
    end_time = datetime.now()
    print(colored('Duration time: {} seconds '.format(end_time - start_time), "blue"), "\n start_time:", start_time,
          "\n", "end_time  :", end_time)