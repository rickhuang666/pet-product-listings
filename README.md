# pet-product-listings

The purpose of this program is to automatically capture all WellPet product listings and prices from major retailers that have online presences. 

The basis of the scripts start from Chewy.com. 

The general idea is to use BeautifulSoup to loop through all pages of WellPet products, and for pages with interactive buttons to select product variations, use Selenium to simulate button clicks then use BeautifulSoup to extract relevant information from HTML components. For those pages without any clickable buttons, the BeautifulSoup will be used to extract the HTML content.

The information is stored in a Pandas data frame and will be casted out as CSV files. 