import logging
import requests

class WeatherDataExtractor:

    def __init__(self, api_token):
        """Class constructor

        Attributes:
            api_token: A string with the public key 
        """
        
        self.base_url = "https://api.dataplatform.knmi.nl/open-data/v1"
        self.headers = {"Authorization": api_token}
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("logs/debug.log", mode="w"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

    
    def __get_data(self, url: str, params=None):
        """Main private method to call the api

        Args:
            url (str): endpoint 
            params (dict, optional): dictionary with parameters. Defaults to None.

        Returns:
            object: response object in json format
        """
        
        requests.packages.urllib3.disable_warnings()
        return requests.get(url, headers=self.headers, params=params, verify=False).json()


    def __get_filenames(self, dataset_name: str, dataset_version: str, params: dict):
        """Private method to retrieve the list of available files

        Args:
            dataset_name (str): the name of the dataset
            dataset_version (str): the verion of the dataset
            params (dict): additional parameters

        Returns:
            object: response in json format
        """
        
        return self.__get_data(
            f"{self.base_url}/datasets/{dataset_name}/versions/{dataset_version}/files",
            params=params
        )
    

    def get_dataset_file(self, dataset_name: str, dataset_version: str, file_name: str):
        """Retrieves and saves the database file in the `data` folder.
        
        Args:
            dataset_name (str): name of the dataset
            dataset_version (str): version of the dataset
            file_name (str): filename of the dataset
        """
        
        # fetch the download url and download the file
        response = self.__get_data(
            f"{self.base_url}/datasets/{dataset_name}/versions/{dataset_version}/files/{file_name}/url"
        )
        download_url = response["temporaryDownloadUrl"]

        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open("data/" + file_name, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except Exception:
            self.logger.exception("Unable to download file using download URL")
            
        self.logger.info(f"Successfully downloaded dataset file to data/{file_name}")


    def get_latest_filename(self,  dataset_name: str, dataset_version: str):
        """Retrieves the latest filename of a given dataset 

        Args:
            dataset_name (str): the name of the dataset
            dataset_version (str): the version of the dataset

        Returns:
            str: a string with the filename
        """
        
        # sort the files in descending order and only retrieve the first file
        params = {"maxKeys": 1, "orderBy": "created", "sorting": "desc"}
        response = self.__get_filenames(dataset_name, dataset_version, params)

        if "error" in response:
            self.logger.error(f"Unable to retrieve list of files: {response['error']}")
            return

        latest_file = response["files"][0].get("filename")
        self.logger.info(f"Latest file is: {latest_file}")
        return latest_file
    

    def list_files(self, download_url: str, filename: str):
        """Shows a list of available files

        Args:
            download_url (str): download url
            filename (str): filename
        """
        
        try:
            with requests.get(download_url, stream=True) as r:
                r.raise_for_status()
                with open(filename, "wb") as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
        except Exception:
            self.logger.exception("Unable to download file using download URL")
            self.logger.exit(1)

        self.logger.info(f"Successfully downloaded dataset file to {filename}")


    