import requests
from bs4 import BeautifulSoup
import sys
import os

REQ_HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.8',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'
}

def clean_dict(property_dict):
    """For each property, creates a new dictionary of only the desired keys.
    If a Key:value does not exist for the property, the value will be None"""
    cleaned_dict = {}
    for key in DESIRED_KEYS:
        try:
            cleaned_dict[key] = property_dict[key]
        except KeyError:
            cleaned_dict[key] = None

    return cleaned_dict

def get_price(soup):
    """Extracts the property's price (as an int) from the soup object"""
    price_wrapped = soup.find_all(class_="Text-c11n-8-62-5__sc-aiai24-0 hdp__sc-b5iact-0 frfoXM fAzOKk")
    price_wrap = price_wrapped[0]
    price = price_wrap.get_text()
    return int(price.replace(",", "").replace("$", ""))

def get_address(soup):
    """Extracts the property's address (as an string) from the soup object"""
    address_wrapped = soup.find(id="ds-chip-property-address", class_="Text-c11n-8-62-5__sc-aiai24-0 StyledHeading-c11n-8-62-5__sc-ktujwe-0 kZKvMY")
    return address_wrapped.get_text().replace("\xa0", " ")

def single_scrape(url):
    """Input: the url of an individual property.
    Output: Dictionary of the properties relevent facts and features"""
    page = requests.get(url, headers=REQ_HEADERS)
    # print("Page Status Code:", page.status_code)

    soup = BeautifulSoup(page.content, 'html.parser')

    price = get_price(soup)
    address = get_address(soup)

    # Get a list of all facts and features listed.
    facts_and_features = soup.findAll(class_="Text-c11n-8-62-5__sc-aiai24-0 kZKvMY")
    fnfs = []
    for f in facts_and_features:
        fnfs.append(f.get_text())
    # Move these into a dictionary for proper storage
    fnfs_dict = {'Property url': url,'Address' : address , 'Price':price}
    for f in fnfs:
        key = f[:f.find(':')]
        value = int(f[f.find(':')+1 : ].strip()) if (f[f.find(':')+1 : ].strip()).isdigit() else f[f.find(':')+1 : ].strip()
        fnfs_dict[key] = value

    # Clean the dictionary for  only the desired values
    fnfs_cleaned = clean_dict(fnfs_dict)
    return fnfs_cleaned


# These are the property properties that we are interested in
DESIRED_KEYS = ['Property url',
                'Address', 'Price',
                'Bedrooms',
                'Bathrooms',
                'Full bathrooms',
                'Basement',
                'Flooring',
                'Appliances included',
                'Total interior livable area',
                'View description',
                'Parking features',
                'Home type',
                'New construction',
                'Year built',
                'Community features',
                'Region',
                'Has HOA']


