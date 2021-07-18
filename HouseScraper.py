"""
@Daniel Bozinovski

Description: Scrapes House Data & saves it to a .csv file in the current repository
"""

# Imports
from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import itertools
import matplotlib.pyplot as plt
import seaborn as sns
sns.set()

# Headers
agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


url = "https://www.domain.com.au/sale/?sort=dateupdated-desc&state=nsw&page=1"
res = get(url, headers=agent)  # Fetch data

# Create parser
htmlSoup = BeautifulSoup(res.text, 'html.parser')

# houses = htmlSoup.find_all('div', class_='css-1ctih3l')
houses = htmlSoup.find_all('div', class_='css-qrqvvg')

first = houses[0]

price = first.find('p', class_='css-mgq8yx').text
price = int(price.replace(',', '').replace('$', ''))

suburb = first.find('span', {"itemprop": "addressLocality"}).text
region = first.find('span', {"itemprop": "addressRegion"}).text
postcode = first.find('span', {"itemprop": "postalCode"}).text
address = first.find('span', {"itemprop": "streetAddress"}).text

propertyType = first.find('span', class_="css-693528").text

print(propertyType)
