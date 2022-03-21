import requests
from bs4 import BeautifulSoup
import sys
import os
from config import *
import logging

# Setup logger for outputting to stdout
logger = logging.getLogger('stdout to log')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(message)s')

# Create a stream handler for handling the stdout
stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.DEBUG)
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

def clean_dict(property_dict, desired_features):
    """
    For each property, creates a new dictionary of only the desired keys.
    If a Key:value does not exist for the property, the value will be None
    """
    cleaned_dict = {}
    for key in desired_features:
        try:
            cleaned_dict[key] = property_dict[key]
        except KeyError:
            cleaned_dict[key] = None
    return cleaned_dict

def get_price(soup):
    """
    Extracts the property's price (as an int) from the soup object
    """
    price_wrapped = soup.find_all(class_="Text-c11n-8-62-5__sc-aiai24-0 hdp__sc-b5iact-0 frfoXM fAzOKk")
    price_wrap = price_wrapped[0]
    price = price_wrap.get_text().split('from ')[-1]
    return int(price.replace(",", "").replace("$", ""))
def get_address(soup):
    """Extracts the property's address (as an string) from the soup object"""
    address_wrapped = soup.find(id="ds-chip-property-address", class_="Text-c11n-8-62-5__sc-aiai24-0 StyledHeading-c11n-8-62-5__sc-ktujwe-0 kZKvMY")
    return address_wrapped.get_text().replace("\xa0", " ")

def scrape_property(url, desired_features):
    """
    Scrapes an individual
    :param url: the url of an individual property.
    :param desired_features: chosen features to retrieve from dataset of property info
    :return: Dictionary of the properties relevent facts and features
    """
    page = requests.get(url, headers=PROPERTY_REQ_HEADERS)
    if page.status_code == 200:
        logger.info(f"Property information scraped successfully --- URL: {url}")
    else:
        logger.error(f"Property scrape unsuccessful --- URL: {url}")
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
    fnfs_cleaned = clean_dict(fnfs_dict, desired_features)
    return fnfs_cleaned