# src/myproject/scraper.py
import requests
from bs4 import BeautifulSoup
import logging
from tenacity import retry, stop_after_attempt, wait_fixed
from myproject.compliance import is_allowed

logger = logging.getLogger(__name__)

@retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
def fetch_page_html(url):
    """
    Fetches page HTML from the URL with retries and ensures robots.txt compliance.
    """
    if not is_allowed(url):
        raise PermissionError(f"Scraping disallowed for URL: {url}")
    
    logger.debug(f"Attempting to fetch page content from {url}")
    response = requests.get(url)
    response.raise_for_status()  # This will raise an HTTPError on bad response.
    logger.info("Page fetched successfully")
    return response.text

def parse_table(html):
    """
    Parses the first wikitable found in the HTML content.
    """
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"class": "wikitable"})
    if table is None:
        logger.error("No wikitable found on the page.")
        raise ValueError("No wikitable found.")
    logger.debug("Wikitable found; processing table rows.")
    rows = table.find_all("tr")[1:]  # Skip the header row.
    return rows

def parse_table_rows(rows):
    """
    Extracts and cleans data from table rows.
    """
    data_rows = []
    for row in rows:
        columns = row.find_all("td")
        if len(columns) >= 4:
            country = columns[0].text.strip()
            city = columns[1].text.strip()
            population = columns[2].text.strip()
            area = columns[3].text.strip()
            
            # Clean population data.
            population_clean_str = population.replace(",", "").replace(" ", "")
            population_clean = int(population_clean_str) if population_clean_str.isdigit() else 0

            # Clean area data.
            area_clean_str = area.replace(" km²", "").replace(",", "").strip()
            try:
                area_clean = float(area_clean_str)
            except ValueError:
                area_clean = 0

            data_rows.append({
                "Country": country,
                "Core City": city,
                "Population": population_clean,
                "Area": area_clean
            })
    logger.info("Parsed table rows successfully")
    return data_rows

def create_countries_dictionary(data_rows):
    """
    Groups the rows by country, adding population density calculations.
    """
    countries_dict = {}
    for data in data_rows:
        country = data["Country"]
        city = data["Core City"]
        population = data["Population"]
        area = data["Area"]

        if country not in countries_dict:
            countries_dict[country] = []
        
        countries_dict[country].append({
            "City": city,
            "Population": population,
            "Area": area,
            "Population Density": population / area if area != 0 else 0
        })
    logger.debug("Countries dictionary created")
    return countries_dict
