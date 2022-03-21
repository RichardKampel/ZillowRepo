#!/usr/bin/env python3

import requests
import sys
import argparse
from bs4 import BeautifulSoup
import re
from SinglePropertyScraper import *
from config import *
from schema_SQL import create_db_schema
from SQL_inserts import *


def print_dict_nicely(dict, row_title_key):
    """
    Prints dictionary nicely
    :param dict: dict to print
    :param row_title_key: key in dict to be used as the title of each row upon printing
    """
    print('')
    for key in dict:
        print(f'{dict[key][row_title_key].ljust(60)}: {dict[key]}')
    print('\n')


class ZillowSearch:
    """
    Class whose objects represent individual searches for properties on Zillow
    Attributes:
         - search_url: url of the search (for a specific location)
         - name: name of location searched
    """

    def __init__(self, search_url, desired_features):
        """
        Initializes ZillowSearch object with both its parameters
        :param search_url: url of the search
        Creates two attributes:
            - url: url of the search
            - properties_info_dict: dictionary of properties (keys) and each property's information (values)
        """
        self.url = search_url
        self.search_title = None
        self.property_urls_list = []
        self.properties_info_dict = {}
        self.desired_features = desired_features

    def set_search_title(self, title):
        """
        Sets search title of search object to reflect the location 'registered' by Zillow upon the search's execution
        (ex1. search query = 'miami' ---> search title = 'Real & Estate & Homes for Sale in Miami, FL')
        (ex2. search query = 'adsfdgsdgh' ---> search title = 'Real & Estate & Homes for Sale (location undetermined))
        :param title: title to which the search value will be set
        """
        self.search_title = title

    def create_properties_info_dict(self):
        """
        Creates properties_info_dict, a dictionary of properties (keys) and each property's information (values)
        """
        self.properties_info_dict = {}
        for property_url in self.property_urls_list:
            self.properties_info_dict[property_url] = scrape_property(property_url, self.desired_features)

    def __str__(self):
        """
        When zsearch object converted to string, dictionary of property information (for given search) printed neatly
        and automatically
        """
        print_dict_nicely(self.properties_info_dict, 'Address')
        return f'{self.properties_info_dict}'


class ZillowScraper:
    """
    Class whose object represents the project's singular scraper (only one ZillowScraper object created)
    Attributes:
         - property_urls_dict: dictionary of searches/locations searched (keys) and the property urls for each of the
           properties in the given search (e.g. {"https://...manhattan": [prop_url1, prop_url2], ...} )
    """
    property_url_class_in_search = 'list-card-link list-card-link-top-margin'

    def __init__(self):
        """
        Initializes single and only ZillowScraper object
        """
        self.property_urls_dict = {}  # {search1: [prop_url1.1, ...], search2: [prop_url2.1, ...], }

    def scrape_search_for_property_urls(self, zsearch_obj):
        """
        Scrapes url of a ZillowSearch object (e.g. ZillowSearch.url) for the urls of each property in the search result
        :param zsearch_obj: ZillowSearch object
        """
        with requests.Session() as session:
            r = session.get(zsearch_obj.url, headers=SEARCH_REQ_HEADERS)
        soup = BeautifulSoup(r.content, 'html.parser')
        # Set search title (location of search)
        if soup.select('h1.search-title')[0].text.strip() != 'Real Estate & Homes For Sale':
            zsearch_obj.set_search_title(soup.select('h1.search-title')[0].text.strip())
        # Create list of property URLs for searched location
        # Standard bs4 method gave impartial data --> convert html to str and parse for URL w/ format: https://..._zpid/
        for elem in soup('script'):
            if '_zpid/' in str(elem.contents):
                zsearch_obj.property_urls_list += [string for string in re.split(r'"', str(elem.contents[0])) if
                                                  '_zpid/' in string and string not in zsearch_obj.property_urls_list]
        self.property_urls_dict[zsearch_obj] = zsearch_obj.property_urls_list


def parse_arguments():
    """
    Parse arguments using the argparse library
    Set two parameters for scraping real estate information
         (1) locations to search for properties (e.g. Miami)
         (2) the desired property features to retrieve (e.g. # bathrooms)
    :return args.search_locs, desired_features: tuple of both parameters described directly above (in order)
    """
    parser = argparse.ArgumentParser(description='Web scrape Zillow website')
    parser.add_argument('-A', help='collect all data', action='store_true')
    parser.add_argument('-u', help='property url', action='store_true')
    parser.add_argument('-p', help='collect property price', action='store_true')
    parser.add_argument('-r', help='collect num bedrooms', action='store_true')
    parser.add_argument('-b', help='collect # of bathrooms', action='store_true')
    parser.add_argument('-a', help='collect address', action='store_true')
    parser.add_argument('-l', help='collect location', action='store_true')
    parser.add_argument('-s', '--search_locs', nargs='+', help='<Required> Search following locs', required=True)
    args = parser.parse_args()
    if args.u or args.r or args.b or args.a or args.l:
        if args.A:
            raise ValueError("-A flag used in conjunction with feature-specific flags (e.g. -a, -r)")
        desired_features = []
        if args.u:
            desired_features.append('Property URL')
        if args.r:
            desired_features.append('Bedrooms')
        if args.b:
            desired_features.append('Bathrooms')
        if args.a:
            desired_features.append('Address')
        if args.l:
            desired_features.append('Locale/Region')
    else:
        desired_features = PROPERTY_FEATURES
    return args.search_locs, desired_features


def main():
    """
    Main scraper function for extracting data from properties that appear in different searches on Zillow.com
    """
    # Parse arguments; set the (1) locations to search for properties and (2) the desired property features to retrieve
    search_locs, desired_features = parse_arguments()
    # Create list of search URLs for each search loc
    search_urls = ['https://www.zillow.com/homes/' + loc + '_rb/' for loc in search_locs]
    # Initialise ZillowScraper object
    scraper = ZillowScraper()
    # Create list of Z-Search objects, one for each url provided.
    zsearch_obj_list = [ZillowSearch(url, desired_features) for url in search_urls]
    logger.info(f"{len(zsearch_obj_list)} search objects created successfully: {search_locs}")
    print("PROPERTY INFO FOR ALL PROPERTIES:\n\n")
    for zsearch_obj in zsearch_obj_list:
        print(zsearch_obj)
    for i in range(len(zsearch_obj_list)):
        # Creates list of property URLs for searched location
        scraper.scrape_search_for_property_urls(zsearch_obj_list[i])
        # Creates a dictionary of property-specific information, for each of the properties in a given search result
        zsearch_obj_list[i].create_properties_info_dict()
        # Prints all property-specific data for each property in a given search result
    # # Print property data for all properties searched



    # Create SQL Database
    create_db_schema()
    for zsearch_obj in zsearch_obj_list:
        add_scrape_to_scrapes_tbl(zsearch_obj.search_title)
        scrape_id = get_current_scrape_id()
        for property in zsearch_obj.properties_info_dict.values():
            print(zsearch_obj.properties_info_dict)
            print(zsearch_obj.properties_info_dict.values())
            add_property_to_properties_tbl(property, scrape_id)

if __name__ == "__main__":
    main()