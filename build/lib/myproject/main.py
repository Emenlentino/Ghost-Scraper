# src/myproject/main.py

import logging
import json
from myproject.scraper import fetch_page_html, parse_table, parse_table_rows, create_countries_dictionary
from myproject.data_handler import load_data, compare_and_save
from myproject.config import URL, DATA_FILE
from myproject.logger import setup_logging

def main():
    setup_logging()  # Initialize rich logging for the application.
    logging.debug("Starting application execution...")

    try:
        html = fetch_page_html(URL)
        rows = parse_table(html)
        data_rows = parse_table_rows(rows)
        countries_dict = create_countries_dictionary(data_rows)
        
        existing_data = load_data(DATA_FILE)
        updated = compare_and_save(countries_dict, existing_data, DATA_FILE)
        if updated:
            logging.info("Data updated successfully.")
        else:
            logging.info("No updates required; stored data remains current.")
        
        # Optionally, output the final result.
        print(json.dumps(countries_dict, indent=4))
    except Exception as e:
        logging.exception("An error occurred during execution.")

if __name__ == "__main__":
    main()
