## Election Scraper
## Project Information
## Author: Matouš Kopáček

## About
This script scrapes election data from the website https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ and saves the results into a CSV file.

## Usage
To run the script, use the following command in the terminal:
python Election_scraper.py <link> <csv_file.csv>

Make sure to install the required dependencies using:
pip install beautifulsoup4 requests

The script will generate a CSV file containing election data for each city in the specified territory. The columns include city code, location, registered voters, envelopes issued, valid votes, and votes for various political parties.
