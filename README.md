
## Webscrape of Zillow.com in Python.

input requirements: Initial search urls for areas of interest.
Output: a Dictionary of the data of each of the properties in the regions provided.
Project coded in: Python3, with the following libraries: requests, bs4.

# Goal
Given only a list urls from searches by area: scrape through the properties listed retrieve and store the most relevent data on each.

The code enclosed achieves the desired result by performing the following broad steps:
1) Enter Zillow.com at the inputted urls, which should be results of searches of areas of interest
2) scrape through these pages for the urls of the properties listed on that search
3) go into each of these properties and extract the most important variables of each property, listed below.
4) the data will be stored in a Dictionary form for the time being, until being transfered to a database at a later date.

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
## Environment Variables and installation

To run this project, you will need to add the following libraries to your Python3 base:
- bs4
- requests

For further installation details see the accompanying file: **requirements.txt**

*3 seperate python scripts are enclosed.
They all need to be callable for the program to run.*
This was done to keep the functions which are invlolved in different parts of the program seperate
and the code more readable.

## Authors

- Noam Goldberg
- Richard Kampel


## Project Status

Stage One -     Webscraper      : Complete
Next Stage -    Database Design : Ongoing

## Usage Example

You may input a list of urls from searches of different regions in your configurations.

We have used these two searches, Manhattan and Miami, respectively, which can be input as parameters:
https://www.zillow.com/homes/Manhattan,-New-York,-NY_rb/ https://www.zillow.com/homes/Miami,-FL_rb/