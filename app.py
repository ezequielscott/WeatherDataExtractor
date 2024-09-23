
import os
from weather_extractor import WeatherDataExtractor
from datetime import datetime

import logging

if __name__ == '__main__':

    logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("logs/debug.log", mode="w"),
                logging.StreamHandler()
            ]
        )
    
    logging.info("Weather Data Extractor")
    
    api_key = os.environ['API_KEY']
    dataset_name = "Actuele10mindataKNMIstations"
    dataset_version = "2"

    logging.info(f"Fetching latest file of {dataset_name} version {dataset_version}")

    # init the extractor
    wext = WeatherDataExtractor(api_key)

    filename = wext.get_latest_filename(dataset_name, dataset_version)
    
    logging.info(f"Latest filename: {filename}")

    wext.get_dataset_file(dataset_name, dataset_version, filename)

    #connection = psycopg2.connect(database="weather", user='root', password='password', host="postgres_db", port=5432)

    