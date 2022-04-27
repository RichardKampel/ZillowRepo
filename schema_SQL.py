from datetime import datetime
from config import *
from Gis_API import get_latlng


def add_scrape_to_scrapes_tbl(search_title):
    # CURSOR.execute("USE zillow_db;")
    scrapes_insert_sql = "INSERT INTO scrapes (scrape_location, date_time) VALUES (%s, %s);"
    today_str = datetime.now().strftime('%Y-%m-%d, %H:%M:%S')
    CURSOR.execute(scrapes_insert_sql, (search_title, today_str))
    connection.commit()


def get_current_scrape_id():
    # CURSOR.execute("USE zillow_db;")
    max_sql = "SELECT max(scrape_id) FROM scrapes;"
    CURSOR.execute(max_sql)
    max_scrape_id = CURSOR.fetchone()['max(scrape_id)']
    return max_scrape_id


def get_current_property_id():
    # CURSOR.execute("USE zillow_db;")
    current_property_id_sql = "SELECT max(property_id) FROM properties;"
    CURSOR.execute(current_property_id_sql)
    curr_property_id = CURSOR.fetchone()['max(property_id)']
    return curr_property_id


def entry_exists(property_url):
    # CURSOR.execute("USE zillow_db;")
    p_url_search_SQL = "SELECT property_id FROM properties WHERE property_url = %s"
    CURSOR.execute(p_url_search_SQL, property_url)
    try:
        property_id = CURSOR.fetchone()['property_id']
    except TypeError:
        return False
    return property_id


def add_property_to_properties_tbl(property):
    # CURSOR.execute("USE zillow_db;")
    if entry_exists(property['Property url']):
        pass
    else:
        scrape_id = get_current_scrape_id()
        properties_insert_sql = """INSERT INTO properties (scrape_id, Property_url, Address, Price, Bedrooms, Bathrooms,
        Full_bathrooms, Basement, Flooring, Appliances_included, Total_interior_livable_area, View_description, 
        Parking_features, Home_type, New_construction, Year_built, Community_features, Region, Has_HOA) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        property_data = [scrape_id]
        for key in PROPERTY_FEATURES:
            try:
                property_data.append(property[key])
            except KeyError:
                property_data.append(None)
        CURSOR.execute(properties_insert_sql, property_data)
        connection.commit()
        add_lat_lng_to_lat_lng_tbl(get_current_property_id(), property['Address'])


def add_lat_lng_to_lat_lng_tbl(property_id, address):
    lat_lng_insert_sql = """INSERT INTO lat_lng (property_id, lat, lng)
    VALUES (%s, %s, %s)"""
    lat_lng = get_latlng(address)
    id_lat_lng = [property_id, lat_lng[0], lat_lng[1]]
    CURSOR.execute(lat_lng_insert_sql, id_lat_lng)
