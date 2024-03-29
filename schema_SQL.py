from config import *

create_db_sttmnt = "CREATE DATABASE IF NOT EXISTS zillow_db;"
use_db_sttment = "USE zillow_db;"

create_scrapes_table_sttmnt = "CREATE TABLE IF NOT EXISTS scrapes (\
                                scrape_id INT AUTO_INCREMENT PRIMARY KEY,\
                                scrape_location VARCHAR(250),\
                                date_time DATETIME\
                              );"

create_properties_table_sttmnt = """CREATE TABLE IF NOT EXISTS properties (
										property_id		INT AUTO_INCREMENT PRIMARY KEY,
										scrape_id		INT,
										Property_url	VARCHAR(250),
							            Address 		VARCHAR(250),
							            Price 			FLOAT,
							            Bedrooms 		INT,
							            Bathrooms 		FLOAT,
							            Full_bathrooms 	INT,
							            Basement 		VARCHAR(250),
							            Flooring 		VARCHAR(250),
							            Appliances_included VARCHAR(250),
							            Total_interior_livable_area VARCHAR(250),
							            View_description VARCHAR(250),
							            Parking_features VARCHAR(250),
							            Home_type 		VARCHAR(250),
							            New_construction VARCHAR(250),
							            Year_built 		VARCHAR(250),
							            Community_features VARCHAR(250),
							            Region 			VARCHAR(250),
							            Has_HOA 		VARCHAR(250)
							            );"""

def create_db_schema():
     connection = pymysql.connect(host=HOST,
                                user=USER,
                                password=PASSWORD,
                                cursorclass=pymysql.cursors.DictCursor)

     with connection.cursor() as cursor:
        cursor.execute(create_db_sttmnt)

        cursor.execute(use_db_sttment)

        cursor.execute(create_scrapes_table_sttmnt)
        cursor.execute(create_properties_table_sttmnt)
        connection.commit()



