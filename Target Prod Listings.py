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
# If a brand doesnt have any sub page, return ['0']
page = soup.find('span', attrs={'class':'h-text-lg'}) or ['0']
page_check = lambda page: [0] if page == ['0'] else list(range(int(list(page.text.split())[-1])))
page_cnt = page_check(page)


# Target uses multiples of 24 as page number in URL. Define page numbers as Nao
for p in page_cnt:
    p = 24 * p
    all_page.append(p)

driver1.quit()

# Creating a list for all pages under one brand
all_listing = []
for i in all_page:
    listing = start_url + '?Nao=' + str(i)
    all_listing.append(listing)

# Getting all product URLs for each listing page.
# Product URL has similar HTML element class/tag to irrelevant URLs. Use a product_link to hold all URLs found on page.
product_link = []
for listing in all_listing[:1]:
    driver2 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
    driver2.get(listing)
    time.sleep(2)
    driver2.get(listing)
    time.sleep(3)
    driver2.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    page_source = driver2.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    for url in soup.select('.h-display-flex > a'):
        product_link.append(url['href'])
    driver2.quit()

# Create a new list to hold true product URLs, it starts with /p/
product_link = ['https://www.target.com' + i for i in product_link if i.startswith('/p/')]

for link in product_link[2:3]:
    driver3 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
    driver3.get(link)
    time.sleep(2)
    driver3.get(link)
    time.sleep(3)
    page_source = driver3.page_source
    time.sleep(3)
    soup = BeautifulSoup(page_source, 'html.parser')
    time.sleep(1)
    # Check if a product has variation selection button
    btn_cnt = []
    for btn in soup.findAll('div', attrs={'class':'VariationButton__StyledButtonWrapper-sc-1hf3dzx-0 gEeRZG'}):
        btn_cnt.append(str(btn))
    btn_list = list(range(len(btn_cnt)+1))[1:]
    if len(btn_cnt) == 0:

