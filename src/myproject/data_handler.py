# src/myproject/data_handler.py
import json
import os
import logging

logger = logging.getLogger(__name__)

def save_data(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)
    logger.info(f"Data successfully saved to {filename}")

def load_data(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            data = json.load(f)
        logger.info(f"Data loaded from {filename}")
        return data
    logger.warning(f"Data file '{filename}' not found; returning empty dictionary.")
    return {}

def compare_and_save(new_data, existing_data, filename):
    if new_data != existing_data:
        logger.info("New data detected; updating file.")
        save_data(new_data, filename)
        return True
    logger.info("No differences detected; no update needed.")
    return False
