# src/myproject/scraper.py

import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def fetch_page_html(url):
    logger.debug(f"Fetching page content from {url}")
    response = requests.get(url)
    response.raise_for_status()  # Raise an exception if the HTTP request returned an unsuccessful status code.
    logger.info("Page fetched successfully")
    return response.text

def parse_table(html):
    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find('table', {'class': 'wikitable'})
    if table is None:
        logger.error("No wikitable found on the page")
        raise ValueError("No wikitable found in the page.")
    logger.debug("Wiki table located; processing rows")
    rows = table.find_all('tr')[1:]  # Skip the header row
    return rows

def parse_table_rows(rows):
    data_rows = []
    for row in rows:
        columns = row.find_all('td')
        if len(columns) >= 4:
            country = columns[0].text.strip()
            city = columns[1].text.strip()
            population = columns[2].text.strip()
            area = columns[3].text.strip()
            
            # Clean up population: remove commas and spaces. Use 0 if not a valid digit.
            population_clean_str = population.replace(',', '').replace(' ', '')
            population_clean = int(population_clean_str) if population_clean_str.isdigit() else 0

            # Clean up area: remove ' km²', commas; try converting to float.
            area_clean_str = area.replace(' km²', '').replace(',', '').strip()
            try:
                area_clean = float(area_clean_str)
            except ValueError:
                area_clean = 0

            data_rows.append({
                'Country': country,
                'Core City': city,
                'Population': population_clean,
                'Area': area_clean
            })
    logger.info("Table rows parsed successfully")
    return data_rows

def create_countries_dictionary(data_rows):
    countries_dict = {}
    for data in data_rows:
        country = data['Country']
        city = data['Core City']
        population = data['Population']
        area = data['Area']
        
        if country not in countries_dict:
            countries_dict[country] = []
        
        countries_dict[country].append({
            'City': city,
            'Population': population,
            'Area': area,
            'Population Density': population / area if area != 0 else 0
        })
    logger.debug("Countries dictionary generated")
    return countries_dict
