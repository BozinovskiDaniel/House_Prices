"""
@Daniel Bozinovski

Description: Scrapes House Data & saves it to a .csv file in the current repository
"""

# Imports
import os
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

# Lists that will form our data frame
prices = []
suburbs = []
regions = []
pCodes = []
addresses = []
size = []
propertyTypes = []
beds = []
baths = []
parking = []
urls = []


def getHouseData(propType, state):
    # Loop to scrape over pages
    numPages = 0

    for page in range(1000):

        numPages += 1

        url = f"https://www.domain.com.au/sale/?ptype={propType}&sort=dateupdated-desc&state={state}&page={numPages}"
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
                addresses.append(
                    address.text) if address else addresses.append("")

                # Property Type
                propertyType = house.find('span', class_="css-693528")

                propertyTypes.append(
                    propertyType.text) if propertyType else propertyTypes.append("")

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

        else:
            break

        sleep(randint(1, 2))  # sleep for 1-2 seconds between each page

    print('You scraped {} pages containing {} properties.'.format(
        numPages, len(prices)))


getHouseData("apartment", "nsw")
getHouseData("house", "nsw")
getHouseData("townhouse", "nsw")
getHouseData("retirement", "nsw")

# Convert to pandas data frame and save as .csv
cols = ['Price', 'Suburb', 'Region', 'Postcode', 'Address',
        'Size (m^2)', 'Property Type', 'Beds', 'Baths', 'Parking', 'URL']

houseData = pd.DataFrame({'Price': prices, 'Suburb': suburbs, 'Region': regions, 'Postcode': pCodes,
                          'Address': addresses, 'Size (m^2)': size, 'Property Type': propertyTypes, 'Beds': beds,
                          'Baths': baths, 'Parking': parking, 'URL': urls})[cols]

cwd = os.getcwd()
path = cwd + "/HouseData.csv"
houseData.to_csv(path)
