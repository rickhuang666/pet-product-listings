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

# Use Selenium to get buttons through all pages.
price_data = []
date = date.today().strftime('%m/%d/%Y')

for test_url in all_url:
    test = BeautifulSoup(requests.get(test_url, headers=headers).content, 'html.parser')

    btn_count = []
    xpath = []

    # Count buttons per page for product variations.
    for btn_cnt in test.findAll('div', attrs={'id': 'vue-portal__sfw-attribute-buttons'}):
        btn = list(range(btn_cnt['data-attributes'].count('"isBuyable":true,"inStock":true,"') + 1))[1:]
        btn_count.append(btn)

    # If a page has no size variation button, then go with soup directly without opening browser by Selenium.
    if len(btn_count) == 0:
        soup = BeautifulSoup(requests.get(test_url, headers=headers).content, 'html.parser')
        for id, auto_ship, price in zip(soup.findAll('div', attrs={'class': 'value js-part-number'}),
                                        soup.findAll('p', attrs={'class': 'autoship-pricing p'}),
                                        soup.findAll('span', attrs={'class': 'ga-eec__price'})):
            chewy_id = ' '.join(id.span.text.split())
            p1 = auto_ship.text.index('(')
            auto_ship = ' '.join(auto_ship.text[:p1].split())
            regular_price = ' '.join(price.text.split())
            price_data.append((date,chewy_id,auto_ship,regular_price))

    # If a page has size variation selector button, open Selenium to simulate button click.
    else:
        driver = webdriver.Chrome(executable_path=r'C:\Users\Rick Huang\Downloads\chromedriver')
        # Getting all buttons' XPATHs.
        for b in btn_count[0]:
            btn_path = '//*[@id="variation-Size"]/div[2]/div[' + str(b) + ']/div/label'
            xpath.append(btn_path)

        for btn in xpath:
            driver.get(test_url)
            time.sleep(5)
            driver.find_element_by_xpath(btn).click()
            time.sleep(3)
            page_source = driver.page_source
            soup = BeautifulSoup(page_source, 'html.parser')
            for id, auto_ship, price in zip(soup.findAll('div', attrs={'class': 'value js-part-number'}),
                                            soup.findAll('p', attrs={'class': 'autoship-pricing p'}),
                                            soup.findAll('span', attrs={'class': 'ga-eec__price'})):
                chewy_id = ' '.join(id.span.text.split())
                p1 = auto_ship.text.index('(')
                auto_ship = ' '.join(auto_ship.text[:p1].split())
                regular_price = ' '.join(price.text.split())
                # Write for loop values to price_data list.
                price_data.append((date,chewy_id,auto_ship,regular_price))
        # Close Selenium when all pages with buttons are looped through.
        driver.quit()
# Convert to Panda DF from price_data list

chewy = pd.DataFrame(price_data, columns=['date','id','auto_ship','regular_price'])

# Export to CSV
chewy.to_csv(r'C:\Users\Rick Huang\Desktop\chewy_price.csv', index=False, header=True)


