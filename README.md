
# Webscrape of Zillow.com in Python.

Input requirements: Initial search urls for areas of interest.
Output: a Dictionary of the data of each of the properties in the regions provided.
Project coded in: Python3, with the following libraries: requests, bs4.

## Goal
Given only a list urls from searches by area: scrape through the properties listed retrieve and store the most relevent data on each.

The code enclosed achieves the desired result by performing the following broad steps:
1) Enter Zillow.com at the inputted urls, which should be results of searches of areas of interest
2) scrape through these pages for the urls of the properties listed on that search
3) go into each of these properties and extract the most important variables of each property, listed below.
4) the data will be stored in an SQL database

List of attributes captured for each property*:
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

*If a property does not have a value for one of these attributes a None will be recorded, in keeping with Python convention.

Additionally, the following information will be captured about each property from the GISGRAPHY API  (https://services.gisgraphy.com/static/leaflet/index.html)
- Latitude
- Longitude

## Environment Variables and Installation

To run this project, you will need to add the following libraries to your Python3 base:
- bs4
- requests


For further installation details see the accompanying file: **requirements.txt**

*3 separate python scripts are enclosed.
They all need to be callable for the program to run.*
This was done to keep the functions which are invlolved in different parts of the program seperate
and the code more readable.

## Running the Program Through the Command Line

Through the implementation of the argparse module, the program (Zillow.py) can be run using the following syntax:

	usage: Zillow.py [-h] [-A] [-u] [-p] [-r] [-b] [-a] [-l] -s SEARCH_LOCS
                 	[SEARCH_LOCS ...]

-h: help tag will print the above usage information for the user's convenience

-s: **REQUIRED** enables the input of one or more locations in which to search for properties and scrape information

-A: will store ALL available property features following the collection of property data from Zillow.com.
** This tag is mutually exlusive from each of the other following tags

The following tags enable the user to select specfic property features that shall be scraped and stored in the database.:
-u: url
-p: price
-r: bedrooms
-b: bathrooms
-a: address
-l: locale/region
The above tags can be used in combination with one another (e.g. -ua --> scrape the url and address of each property)


## Database Set-Up and Design
A SQL database, zillow_db, and schema is created, if it does not already exist.
The database has two tables, scrapes and properties, as documented below.

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





## Authors

- Noam Goldberg
- Richard Kampel


## Project Status

Stage 1  -   Webscraper                	: Complete
Stage 2  -   Database Design          	: Complete
Stage 3  -   Command Line Operability  : Complete
Stage 4  -   Data Storage              		: Complete


## Usage Example

You may input a list of urls from searches of different regions in your configurations.

We have used these two searches, Manhattan and Miami, respectively, which can be input as parameters:
https://www.zillow.com/homes/Manhattan,-New-York,-NY_rb/ https://www.zillow.com/homes/Miami,-FL_rb/

