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
show_more = '//*[@id="tabContent-tab-Details"]/div/button'


all_page = []
price_data = []
date = date.today().strftime('%m/%d/%Y')

# Selenium to simulate page click and show all hidden contents
driver1 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
driver1.get(start_url)
time.sleep(5)
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

print('{:<15}{:<30}{:<100}{:<15}{:<15}{:<10}'.format('date', 'brand', 'product', 'upc', 'price', 'rating'))

for link in product_link:
    driver3 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
    driver3.get(link)
    time.sleep(2)
    driver3.maximize_window()
    driver3.find_element_by_xpath(show_more).click()
    time.sleep(3)
    page_source = driver3.page_source
    time.sleep(1)
    soup = BeautifulSoup(page_source, 'html.parser')
    time.sleep(1)
    # Check if a product has variation selection button
    btn_cnt = []
    for btn in soup.findAll('div', attrs={'class':'VariationButton__StyledButtonWrapper-sc-1hf3dzx-0 gEeRZG'}):
        btn_cnt.append(str(btn))
    btn_list = list(range(len(btn_cnt)+1))[1:]

    if len(btn_cnt) == 0:
        # driver3.find_element_by_xpath(show_more).click()
        time.sleep(1)
        for brand, p_name, UPC, price, rating in zip(soup.findAll('div', attrs={'class': 'styles__ProductDetailsTitleRelatedLinks-h3ukx9-0'}),
                                                     soup.findAll('h1', attrs={'class': 'Heading__StyledHeading-sc-1m9kw5a-0'}),
                                                     soup.findAll('div', attrs={'class': 'Col-favj32-0 hezhbt h-padding-h-default'}),
                                                     soup.findAll('div', attrs={'class': 'style__PriceFontSize-gob4i1-0'}),
                                                     soup.findAll('div', attrs={'class': 'RatingSummary__StyledRating-bxhycp-0'})
                                                     ):
            brand = list(brand.text.split('Shop all '))[-1]
            product = p_name.text.replace(brand + ' ','')
            temp_id = UPC.text.split('UPC: ')[1]
            id = temp_id.split('Item')[0]
            price = price.text
            rating = rating.text
            price_data.append((date, brand, product, id, price, rating))
            print('{:<15}{:<30}{:<100}{:<15}{:<15}{:<10}'.format(date, brand, product, id, price, rating))

    else:
        time.sleep(5)
        for b in btn_list:
            variation = '//*[@id="viewport"]/div[5]/div/div[2]/div[2]/div[3]/div/div[2]/div[' + str(b) + ']/button'
            driver3.find_element_by_xpath(variation).click()
            page_source = driver3.page_source
            time.sleep(2)
            soup = BeautifulSoup(page_source, 'html.parser')
            time.sleep(1)
            for brand, p_name, UPC, price, rating in zip(soup.findAll('div', attrs={'class': 'styles__ProductDetailsTitleRelatedLinks-h3ukx9-0'}),
                                                         soup.findAll('h1', attrs={'class': 'Heading__StyledHeading-sc-1m9kw5a-0'}),
                                                         soup.findAll('div', attrs={'class': 'Col-favj32-0 hezhbt h-padding-h-default'}),
                                                         soup.findAll('div', attrs={'class': 'style__PriceFontSize-gob4i1-0'}),
                                                         soup.findAll('div', attrs={'class': 'RatingSummary__StyledRating-bxhycp-0'})
                                                         ):
                brand = list(brand.text.split('Shop all '))[-1]
                product = p_name.text.replace(brand + ' ', '')
                temp_id = UPC.text.split('UPC: ')[1]
                id = temp_id.split('Item')[0]
                price = price.text
                rating = rating.text
                price_data.append((date, brand, product, id, price, rating))
                print('{:<15}{:<30}{:<100}{:<15}{:<15}{:<10}'.format(date, brand, product, id, price, rating))

    driver3.quit()
