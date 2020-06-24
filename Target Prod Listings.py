import requests
import pandas as pd
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver



# Getting Target brand page.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
# Brand landing page
start_url = 'https://www.target.com/b/blue-buffalo/-/N-ewdj9'

all_page = []


# Selenium to simulate page click and show all hidden contents
driver = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
driver.get(start_url)
time.sleep(8)
page_source = driver.page_source
soup = BeautifulSoup(page_source, 'html.parser')
page = soup.find('span', attrs={'class':'h-text-lg'})
page_cnt = list(range(int(list(page.text.split())[-1])))

# Target uses multiples of 24 as page number in URL
for p in page_cnt:
    p = 24 * p
    all_page.append(p)

driver.quit()

# Creating a list for all URLs under one brand
all_urls = []

for i in all_page:
    url = start_url + '?Nao=' + str(i)
    all_urls.append(url)

