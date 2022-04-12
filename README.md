
# Webscrape of Zillow.com in Python.

Input requirements: areas from which property information will be collected and stored.
Output: a (SQL) database containing the data of each of the properties listed on the first page of the Zillow search results for the provided areas.
Project coded in: Python3, with libraries requests, bs4, and more (complete list can be found in the enclosed requirements.txt file)

## Goal
Given only a list of areas (i.e. Miami,-FL), scrape through the properties listed in the Zillow search results for that area retrieve and store the most relevent data for each property in the first page of the results.

The code enclosed achieves the desired result by performing the following broad steps:
1) Enter [Zillow.com](https://www.zillow.com/) at the inputted urls, which should be results of searches of areas of interest
2) Scrape through these pages for the urls of the properties listed on that search
3) Go into each of these properties and extract the most important variables of each property (see below).
4) Implement the [GISGRAPHY API](https://services.gisgraphy.com/static/leaflet/index.html) to extract the geographical cooordinates of each property (latitude and longitude). 
5) Build an SQL database schema and store all collected data in the database

List of attributes captured for each property from [Zillow.com](https://www.zillow.com/):
- Property url
- Physical Address
- Price
- Bedrooms
- Bathrooms
- Full bathrooms
- Basement
- Flooring
- Appliances included
- Total interior livable area
- View description
- Parking features
- Home type
- New construction
- Year built
- Community features
- Region
- Has HOA

_*If a property does not have a value for one of these attributes a None will be recorded, in keeping with Python convention._

List of attributes captured for each property from the [GISGRAPHY API](https://services.gisgraphy.com/static/leaflet/index.html):
- Latitude
- Longitude

_*These features will be collected in a separate table. See the "Database Set-Up and Design" section below for more information._

## Environment Variables and Installation

To run this project, you will need to add the following libraries to your Python3 base:
- bs4
- requests

_For further installation details see the accompanying file: **requirements.txt**_

There are 6 separate python scripts enclosed in the project files:
 1. Zillow.py
 1. SinglePropertyScraper.py
 1. schema_SQL.py
 1. SQL_inserts.py
 1. GIS_API.py
 1. config.py

This was done to keep the functions which are invlolved in different parts of the program seperate
and the code more readable. **They all need to be callable for the program to run.**

## Running the Program Through the Command Line

Through the implementation of the argparse module, the program (Zillow.py) can be run using the following syntax:

	usage: Zillow.py [-h] [-A] [-u] [-p] [-r] [-b] [-a] [-l] -s SEARCH_LOCS
                 	[SEARCH_LOCS ...]

-h: help tag will print the above usage information for the user's convenience

-s: **REQUIRED** enables the input of one or more locations in which to search for properties and scrape information

-A: will store ALL available property features following the collection of property data from Zillow.com.
 - This tag is mutually exlusive from each of the other following tags

The following tags enable the user to select specfic property features that shall be scraped and stored in the database:
 - -u: url
 - -p: price
 - -r: bedrooms
 - -b: bathrooms
 - -a: address
 - -l: locale/region

_*The above tags can be used in combination with one another (e.g. -ua --> scrape the url and address of each property)_


## Database Set-Up and Design
A SQL database, zillow_db, and schema is created, if it does not already exist.
The database has 3 tables: scrapes, properties, and lat_lng, as documented below.

**scrapes table**
This is a table recording each time and location of the website scrapes.

|COLUMN |  Datatype | Key |
--- | --- | ---
|scrape_id |INT | PRIMARY KEY |
|scrape_location| VARCHAR(250) |
|date_time | DATETIME |
 	
**properties**
For each property in a location scrape, an entry is made in this column.
If the property is already in the database, it will not be duplicated.

|Column Name |  Datatype | Key |
--- | --- | ---
property_id | INT | PRIMARY KEY |
scrape_id | INT  | FOREIGN KEY |
Property_url | VARCHAR(250) |
Address  | VARCHAR(250) |
Price | FLOAT |
Bedrooms  | INT |
Bathrooms | FLOAT |
Full_bathrooms | INT |
Basement | VARCHAR(250) |
Flooring  | VARCHAR(250) |
Appliances_included  | VARCHAR(250) |
Total_interior_livable_area | VARCHAR(250) |
View_description | VARCHAR(250) |
Parking_features  | VARCHAR(250) |
Home_type | VARCHAR(250) |
New_construction  | VARCHAR(250) |
Year_built  | VARCHAR(250) |
Community_features  | VARCHAR(250) |
Region | VARCHAR(250) |
Has_HOA | VARCHAR(250) |

**lat_lng table**
This is a table recording the latitude and longitude of each property, based on its address.

|COLUMN |  Datatype | Key |
--- | --- | ---
|property_id |INT | PRIMARY KEY |
|lat | FLOAT |
|lng | FLOAT |



## Authors

- Noam Goldberg
- Richard Kampel


## Project Status

1. Stage 1  -   Webscraper                	: Complete
1. Stage 2  -   Database Design          	: Complete
1. Stage 3  -   Command Line Operability   : Complete
1. Stage 4  -   Data Storage               : Complete
1. Stage 5  -   API Implementation         : Complete


## Usage Example

You may input a list of locations in your configurations to search multiple regions.

For example, for searching properties in Manhattan and Miami, the arguments can be entered into the command as follows:

	python path/of/Zillow.py -As Miami,-FL Manhattan,-NY
	
Of course, replace the above path with the path in which the Zillow.py file (and other python files) have been downloaded. **Keep in mind that spaces separate arguments. For single arguments in which there is a space, write '-' in place of a space (i.e. New York, NY --> New-York,-NY).**
