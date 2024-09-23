
import os
from extractor import WeatherDataExtractor
from loader import DataLoader

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
    
    database = 'weather'
    user = 'root'
    password = 'password'
    host = 'postgres_db'
    port = 5432
    tablename = 'weather'

    logging.info(f"Fetching latest file of {dataset_name} version {dataset_version}")

    # init the extractor
    wext = WeatherDataExtractor(api_key)
    # retrieve the latest filename
    filename = wext.get_latest_filename(dataset_name, dataset_version)
    logging.info(f"Latest filename: {filename}")
    # retrieve and save the file
    wext.get_dataset_file(dataset_name, dataset_version, filename)
    
    # create a loader
    loader = DataLoader(database, user, password, host, port)
    # load the data
    loader.load(filename, tablename)

    