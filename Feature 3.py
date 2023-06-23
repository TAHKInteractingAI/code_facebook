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

def post_and_get_link_in_group():
    # go through each row
    df = pd.read_csv('Facebook Content.csv')
    num_of_comments = len(df.index)
    for i in range(0, num_of_comments):
        if df['Content'][i] != None:
            # get the link and go to link, assuming all groups here are joined
            driver.get(df['Facebook group'][i])
            # check if group is joined
            time.sleep(3)
            grp_status = len(driver.find_elements_by_xpath('//span[contains(@class, "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5") and text()="Joined"]'))
            if grp_status > 0:
                # find the post button and post
                time.sleep(5)
                text_button = driver.find_element_by_xpath('//div[contains(@class, "oajrlxb2 qu0x051f esr5mh6w e9989ue4 r7d6kgcz rq0escxv nhd2j8a9 p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x i1ao9s8h esuyzwwr f1sip0of abiwlrkh p8dawk7l lzcic4wl bp9cbjyn b3i9ofy5 orhb3f3m czkt41v7 fmqxjp7s emzo65vh j83agx80 btwxx1t3 buofh1pr jifvfom9 l9j0dhe7 idiwt2bm kbf60n1y cxgpxx05 d1544ag0 sj5x9vvc tw6a2znq")]')
                text_button.click()
                time.sleep(2)
                driver.find_element_by_xpath('//div[contains(@class, "_1mf _1mj")]').send_keys(df['Content'][i])
                time.sleep(5)
                post_button = driver.find_element_by_xpath(
                    "/html/body/div[1]/div/div[1]/div/div[4]/div/div/div[1]/div/div[2]/div/div/div/div/div[1]/form/div/div[1]/div/div/div[1]/div/div[3]/div[2]/div/div/div/div[1]")
                post_button.click()
                # find the link to the post (Assume post does not need to be under review)
                time.sleep(5)
                # get today's date as the date posted
                post_date = datetime.today().strftime('%m/%d/%Y')
                # append post date to df
                df.loc[i, 'Date'] = post_date
                #append post link
                df.loc[i, 'Result'] = ''
            else:
                print('Error: You have not joined the group')
                df.loc[i, 'Result'] = 'Not in group'
                df.loc[i,'Date'] = ''
    #get links of posts that have been published
    for i in range(0, num_of_comments):
        # go to group link
        # go to published
        driver.get(df['Facebook group'][i] + "/my_posted_content")
        # check if theres content for that fb group
        if df['Content'][i] != None:
            #check if there are elements in published section
            if len(driver.find_elements_by_xpath('//div[contains(@class, "rq0escxv l9j0dhe7 du4w35lb j83agx80 cbu4d94t pfnyh3mw d2edcug0 aov4n071 bi6gxh9e")]')) > 0:
                postcontent = driver.find_element_by_xpath('div//[contains(@class, "kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql")]').text
                if df['Content'][i] == postcontent:
                    # click on share button
                    driver.find_element_by_xpath('//span[contains(@class, "d2edcug0 hpfvmrgz qv66sw1b c1et5uql lr9zc1uh a8c37x1j fe6kdd0r mau55g9w c8b282yb keod5gw0 nxhoafnm aigsh9s9 d3f4x2em iv3no6db jq4qci2q a3bd9o3v lrazzd5p m9osqain")]').click()
                    time.sleep(2)
                    driver.find_element_by_xpath('//span[contains(@class, "a8c37x1j ni8dbmo4 stjgntxs l9j0dhe7 ltmttdrg g0qnabr5")]').click()
                    post_link = driver.current_url
                    df.loc[i, 'Result'] = post_link
            else:
                df.loc[i, 'Result'] = 'Post is pending/deleted by admin'
    df.to_csv('Facebook Content.csv')

if __name__ == '__main__':
    ### Select using drive profile or not ("Yes" or "No")
    ### Get time of a Python program's execution
    start_time = datetime.now()
    driver = driver_Profile('No')

    # linkedin groups
    results = Login_Facebook()
    if results == True:
        post_and_get_link_in_group()  # returns the post date
        
    time.sleep(1)

    driver.quit()
    ###@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
    ### Get time of a Python program's execution
    ## start_time = datetime.now()
    ## do your work here
    end_time = datetime.now()
    print(colored('Duration time: {} seconds '.format(end_time - start_time), "blue"), "\n start_time:", start_time,
          "\n", "end_time  :", end_time)