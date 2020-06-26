import requests
import pandas as pd
import time
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver



# Getting Target brand page.
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0'}
# Brand landing page
start_url = 'https://www.target.com/p/old-mother-hubbard-classic-crunchy-bac-8217-n-8217-cheez-biscuits-small-oven-baked-dog-treats-20oz/-/A-75662299'

all_page = []

# Selenium to simulate page click and show all hidden contents

show_more = '//*[@id="tabContent-tab-Details"]/div/button'
driver1 = webdriver.Chrome(executable_path=r'C:\Users\rhuang\Downloads\chromedriver')
driver1.get(start_url)
time.sleep(2)
driver1.find_element_by_xpath(show_more).click()
page_source = driver1.page_source
soup = BeautifulSoup(page_source, 'html.parser')

for brand, p_name, UPC, price, rating in zip(soup.findAll('div', attrs={'class':'styles__ProductDetailsTitleRelatedLinks-h3ukx9-0'}),
                                             soup.findAll('h1', attrs={'class':'Heading__StyledHeading-sc-1m9kw5a-0'}),
                                             soup.findAll('div', attrs={'class':'Col-favj32-0 hezhbt h-padding-h-default'}),
                                             soup.findAll('div', attrs={'class':'style__PriceFontSize-gob4i1-0'}),
                                             soup.findAll('div', attrs={'class':'RatingSummary__StyledRating-bxhycp-0'})
                                            ):
    brand = list(brand.text.split('Shop all '))[-1]
    product = p_name.text
    temp_id = UPC.text.split('UPC: ')[1]
    id = temp_id.split('Item')[0]
    package = ' '.join(product.split()[product.split().index('-')+1:])
    price = price.text
    rating = rating.text
    price_data.append((date,brand,product,chewy_id,auto_ship,regular_price,rating))

driver1.quit()