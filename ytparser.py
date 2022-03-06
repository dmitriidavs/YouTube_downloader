import requests
import json
from bs4 import BeautifulSoup


channel_url = 'https://www.youtube.com/c/3blue1brown'
base_url = 'https://www.youtube.com'

# response = requests.get(url)
# soup = BeautifulSoup(response.text, 'lxml')
#
# print(soup.prettify())

# for a in soup.find_all('a', href = True):
#     print("Found URL:", a['href'])

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains
import time

envoke_browser = False
while envoke_browser == False:
    try:
        chrome_options = webdriver.ChromeOptions()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.page_load_strategy = 'none'
        driver = webdriver.Chrome('chromedriver', options=chrome_options)
        driver.maximize_window()
        envoke_browser = True
        print('Driver envoked')
    except:
        print('FAILED to load webdriver, restarting...')

driver.get(url)
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
video_divs = soup.find_all("div", {"id": "dismissible"})

print(len(video_divs))

video_list = []

for el in video_divs:
    for a in el.find_all('a', href = True):
        video_list.append(a['href'])

for v_part_url in video_list:
    video_url_full = base_url + v_part_url
    driver.get(video_url_full)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    # print(soup.prettify())
    time.sleep(2)

    for a in soup.find("div", {"id": "player"}).find_all('a', href = True):
        print(a['href'])

    # print(el.find("div", {"id": "player"}))
    time.sleep(500)

    # break
