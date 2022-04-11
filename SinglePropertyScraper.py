import requests
from bs4 import BeautifulSoup
from config import *


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
    if len(price_wrapped) > 0:
        price_wrap = price_wrapped[0]
        print("price class 1")
    else:
        price_wrapped = soup.find_all(class_="Text-c11n-8-62-5__sc-aiai24-0 dpf__sc-1me8eh6-0 frfoXM fzJCbY")
        if len(price_wrapped) > 0:
            price_wrap = price_wrapped[0]
            print("price class 2")
        else:
            print("could not find price")
            return None
    price = price_wrap.get_text().split('from ')[-1]
    return int(price.replace(",", "").replace("$", ""))


def get_address(soup):
    """Extracts the property's address (as an string) from the soup object"""
    return soup.find("h1").text.strip()


def scrape_property(url, desired_features):
    """
    Scrapes an individual
    :param url: the url of an individual property.
    :param desired_features: chosen features to retrieve from dataset of property info
    :return: Dictionary of the properties relevent facts and features
    """
    page = requests.get(url, headers=PROPERTY_REQ_HEADERS)
    if page.status_code == 200:
        logger.info(f"Page status is 200 --- URL: {url}")
    else:
        logger.error(f"Page status not 200 --- URL: {url}")
    soup = BeautifulSoup(page.content, 'html.parser')
    price = get_price(soup)
    address = get_address(soup)
    # Get a list of all facts and features listed
    facts_and_features = soup.findAll(class_="Text-c11n-8-62-5__sc-aiai24-0 kZKvMY")
    fnfs = []
    for f in facts_and_features:
        fnfs.append(f.get_text())
    # Move these into a dictionary for proper storage
    fnfs_dict = {'Property url': url, 'Address': address, 'Price': price}
    for f in fnfs:
        key = f[:f.find(':')]
        value = int(f[f.find(':')+1:].strip()) if (f[f.find(':')+1:].strip()).isdigit() else f[f.find(':')+1:].strip()
        fnfs_dict[key] = value
    # Clean the dictionary for only the desired values
    fnfs_cleaned = clean_dict(fnfs_dict, desired_features)
    logger.info(f"Info scraped for property: {address}")
    return fnfs_cleaned
