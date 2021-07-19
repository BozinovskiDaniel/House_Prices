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
from time import sleep
from random import randint
sns.set()

# Headers
agent = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}


# url = "https://www.domain.com.au/sale/?sort=dateupdated-desc&state=nsw&page=1"
# res = get(url, headers=agent)  # Fetch data

# # Create parser
# htmlSoup = BeautifulSoup(res.text, 'html.parser')

# # houses = htmlSoup.find_all('div', class_='css-1ctih3l')
# houses = htmlSoup.find_all('div', class_='css-qrqvvg')

# first = houses[0]

# price = first.find('p', class_='css-mgq8yx').text
# # price = int(price.replace(',', '').replace('$', ''))

# suburb = first.find('span', {"itemprop": "addressLocality"}).text
# region = first.find('span', {"itemprop": "addressRegion"}).text
# postcode = first.find('span', {"itemprop": "postalCode"}).text
# address = first.find('span', {"itemprop": "streetAddress"}).text

# propertyType = first.find('span', class_="css-693528").text

# info = first.find_all('span', class_="css-lvv8is")

# beds = info[0].text
# baths = info[1].text
# parking = info[2].text
# squareMetres = info[3].text

# for link in first.find_all('a'):
#     print(link.get('href'))


# Lists that will form our data frame
prices = []
suburbs = []
regions = []
pCodes = []
addresses = []
size = []
propertyType = []
beds = []
baths = []
parking = []
urls = []

# Loop to scrape over pages

numPages = 0

for page in range(2):

    numPages += 1

    url = "https://www.domain.com.au/sale/?sort=dateupdated-desc&state=nsw&page=" + \
        str(numPages)
    res = get(url, headers=agent)  # Fetch data

    htmlSoup = BeautifulSoup(res.text, 'html.parser')  # Create parser
    houses = htmlSoup.find_all('div', class_='css-qrqvvg')  # Get houses

    if houses != []:  # If not empty

        # Loop over houses
        for house in houses:

            # Prices
            price = house.find('p', class_='css-mgq8yx')

            prices.append(price.text) if price else prices.append("")

            # Location
            suburb = house.find('span', {"itemprop": "addressLocality"})
            region = house.find('span', {"itemprop": "addressRegion"})
            postcode = house.find('span', {"itemprop": "postalCode"})
            address = house.find('span', {"itemprop": "streetAddress"})

            suburbs.append(suburb.text) if suburb else suburbs.append("")
            regions.append(region.text) if region else regions.append("")
            pCodes.append(postcode.text) if postcode else pCodes.append("")
            addresses.append(address.text) if address else addresses.append("")

            # Property Type
            propertyType = house.find('span', class_="css-693528")

            propertyType.append(
                propertyType.text) if propertyType else propertyType.append("")

            # Info
            info = house.find_all('span', class_="css-lvv8is")

            if info and len(info) == 4:

                bed = info[0]
                bath = info[1]
                park = info[2]
                squareMetres = info[3]

                beds.append(bed.text) if bed else beds.append("")
                baths.append(bath.text) if bath else baths.append("")
                parking.append(park.text) if park else parking.append("")
                size.append(
                    squareMetres.text) if squareMetres else size.append("")
            else:
                beds.append("")
                baths.append("")
                parking.append("")
                size.append("")

            # Links
            link = (house.find('a')).get('href')

            urls.append(link) if link else urls.append("")

    sleep(randint(1, 2))  # sleep for 1-2 seconds between each page

print(urls)
