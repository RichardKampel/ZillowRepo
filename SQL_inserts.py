import pymysql
from datetime import datetime
from config import *
import pandas as pd


def add_scrape_to_scrapes_tbl(search_title):
    # scrape_id = CURSOR.execute(count).fetchone()
    # scrape_id = SQL_exec(count)[0]['COUNT (*)'] + 1
    # scrapes_insert_py = (scrapes_insert_sql, )
    CURSOR.execute("USE zillow_db;")
    scrapes_insert_sql = "INSERT INTO scrapes (scrape_location, date_time) VALUES (%s, %s);"
    today_str = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    # scrapes_insert_py = scrapes_insert_sql % (search_title, today_str)
    CURSOR.execute(scrapes_insert_sql, (search_title, today_str))
    connection.commit()

def get_current_scrape_id():
    CURSOR.execute("USE zillow_db;")
    max_sql = "SELECT max(scrape_id) FROM scrapes;"
    CURSOR.execute(max_sql)
    max_scrape_id = CURSOR.fetchone()['max(scrape_id)']
    return max_scrape_id

def entry_exists(property_url):
    CURSOR.execute("USE zillow_db;")
    p_url_search_SQL = "SELECT property_id FROM properties WHERE property_url = %s"
    CURSOR.execute(p_url_search_SQL, property_url)
    try:
        property_id = CURSOR.fetchone()['property_id']
        #TypeError: 'NoneType' object is not subscriptable
    except TypeError:
        return False
    return property_id

def add_property_to_properties_tbl(property, scrape_id):
    CURSOR.execute("USE zillow_db;")
    if entry_exists(property['Property url']):
        pass
    else:
        scrape_id = get_current_scrape_id()
        properties_insert_sql = "INSERT INTO properties (scrape_id, Property_url, Address, Price, Bedrooms, Bathrooms, Full_bathrooms, Basement, Flooring, Appliances_included, Total_interior_livable_area, View_description, Parking_features, Home_type, New_construction, Year_built, Community_features, Region, Has_HOA) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        property_data = [scrape_id]
        for key in PROPERTY_FEATURES:
            try:
                property_data.append(property[key])
            except KeyError:
                property_data.append(None)
        CURSOR.execute(properties_insert_sql, property_data)
        connection.commit()