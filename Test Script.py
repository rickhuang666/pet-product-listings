import requests
import pandas as pd
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver



# Getting Target brand page.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
# Brand landing page
start_url = 'https://www.target.com/b/old-mother-hubbard/-/N-1bq97'

all_page = []

# Selenium to simulate page click and show all hidden contents
driver1 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
driver1.get(start_url)
time.sleep(8)
page_source = driver1.page_source
soup = BeautifulSoup(page_source, 'html.parser')
page = soup.find('span', attrs={'class':'h-text-lg'}) or ['0']
page_check = lambda page: [0] if page == ['0'] else list(range(int(list(page.text.split())[-1])))
page_cnt = page_check(page)

