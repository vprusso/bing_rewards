# Python script to accumulate points on Bing rewards.
#
# Requires the Python package "selenium".
#---------------------
import os
import csv
import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common import action_chains, keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

def get_random_line(file_name):
    total_bytes = os.stat(file_name).st_size
    random_point = random.randint(0, total_bytes)
    file = open(file_name)
    file.seek(random_point)
    file.readline()
    return file.readline()

################################################################################
def firefox_profile(is_mobile):

    profile = webdriver.FirefoxProfile()

    if is_mobile == True:
        profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")

    return profile

def bing_search(driver):

    num_search_terms = 30

    bing_search_url = 'https://www.bing.com/?scope=web&mkt=en-US'

    xpaths = { 'bing_search_box'   :   "//*[@id='sb_form_q']",
               'bing_search'       :   "//*[@id='sb_form_go']"
             }

    for i in range(num_search_terms):
        time.sleep(5)
        driver.get(bing_search_url)
        search_term = get_random_line('dictionary.txt')
        driver.find_element_by_xpath(xpaths['bing_search_box']).send_keys(search_term)
        driver.find_element_by_xpath(xpaths['bing_search']).click()

    return driver

def bing_mobile_search(driver):

    profile.set_preference("general.useragent.override", "Mozilla/5.0 (Android 4.4; Mobile; rv:41.0) Gecko/41.0 Firefox/41.0")

    num_search_terms = 30

    bing_rewards_url = 'https://www.bing.com/rewards/dashboard'
    bing_mobile_search_url = 'https://www.bing.com/explore/error?page=rewards-mobile'

    xpaths = { 'bing_search_box'   :   "//*[@id='sb_form_q']",
               'bing_search'       :   "//*[@id='sb_form_go']"
             }

    driver.get(bing_rewards_url)
    time.sleep(5)

    for i in range(num_search_terms):
        time.sleep(5)
        driver.get(bing_mobile_search_url)
        search_term = get_random_line('dictionary.txt')
        driver.find_element_by_xpath(xpaths['bing_search_box']).send_keys(search_term)
        driver.find_element_by_xpath(xpaths['bing_search']).click()

    return driver


def bing_daily_links(driver):
    bing_rewards_url = 'https://www.bing.com/rewards/dashboard'

    driver.get(bing_rewards_url)
    html = driver.page_source

    soup = BeautifulSoup(html)
    reward_links = []
    for link in soup.findAll('a'):
        reward_link = str(link.get('href'))
        if reward_link.startswith("/rewardsapp"):
            reward_link = "https://bing.com" + reward_link
            reward_links.append(reward_link)

    for link in reward_links:
        time.sleep(5)
        driver.get(link)
        time.sleep(5)


def bing_login(user_id,password,is_mobile):

    bing_login_url = 'https://login.live.com/login.srf?wa=wsignin1.0&rpsnv=12&ct=1443495848&rver=6.0.5286.0&wp=MBI&wreply=https:%2F%2Fwww.bing.com%2Fsecure%2FPassport.aspx%3Frequrl%3Dhttps%253a%252f%252fwww.bing.com%252f%253fwlexpsignin%253d1%2526wlexpsignin%253d1&lc=1033&id=264960'
    bing_rewards_url = 'https://www.bing.com/rewards/dashboard'

    xpaths = { 'user_id'   :   "//*[@id='i0116']",
               'password'  :   "//*[@id='i0118']",
               'loginBtn'  :   "//*[@id='idSIButton9']"
             }

    profile = firefox_profile(is_mobile)

    driver = webdriver.Firefox(profile)
    driver.get(bing_login_url)
    time.sleep(5)

    driver.find_element_by_xpath(xpaths['user_id']).clear()
    driver.find_element_by_xpath(xpaths['user_id']).send_keys(user_id)

    driver.find_element_by_xpath(xpaths['password']).clear()
    driver.find_element_by_xpath(xpaths['password']).send_keys(password)

    driver.find_element_by_xpath(xpaths['loginBtn']).click()

    time.sleep(5)
    driver.get(bing_rewards_url)

    return driver


with open('bing_accounts.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        user_id = row[0]
        password = row[1]

        # Regular search
        driver = bing_login(user_id,password,is_mobile=False)
        bing_search(driver)
        driver.quit()

        # Mobile search
        driver = bing_login(user_id,password,is_mobile=True)
        bing_mobile_search(driver)
        driver.quit()

        # Daily links challenge
        driver = bing_login(user_id,password,is_mobile=False)
        bing_daily_links(driver)
        driver.quit()
