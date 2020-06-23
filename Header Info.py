import requests
import pandas as pd
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver




# Getting all Chewy links with WellPet products.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
# WellPet landing page on Chewy.com.
start_url = 'https://www.chewy.com/brands/wellpet-7709?rh=c%3A3312%2Cc%3A7709'
soup_p = BeautifulSoup(requests.get(start_url, headers=headers).content, 'html.parser')
# Count total pages
pages = list(range(1,int(soup_p.select('.cw-pagination__item')[-1].text)+1))

# Extract all page URLs.
all_url = []
for page in pages:
    url = start_url + '&page=' + str(page)
    soup = BeautifulSoup(requests.get(url, headers=headers).content, 'html.parser')
    for link in soup.select('.product-holder > a'):
        link = 'https://www.chewy.com' + link['href']
        all_url.append(link)