import logging
import psycopg2
from netCDF4 import Dataset
import xarray as xr

class DBLoader:

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        """Class constructor

        Attributes:
            api_token: A string with the public key 
        """
        
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("logs/debug.log", mode="w"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        logging.info(f"Connecting to database...")

        try:
            self.connection = psycopg2.connect(database, user, password, host, port)
            cursor = self.connection.cursor()
            cursor.execute("SELECT * FROM pg_catalog.pg_tables;")
            logging.info(cursor.fetchone())
            logging.info(f"Connection OK.")
        except:
            logging.error(f"ERROR connecting to database.")

    
    def load(self, filename:str):

        # root = Dataset("data/"+filename, "r", format="NETCDF4")
        # logging.info("DIMENSIONS:")
        # logging.info(root.dimensions.values())

        # print([d for d in root.dimensions.values()])

        # logging.info("VARIABLES:")
        # logging.info(root.variables.keys())

        # print(root.variables["wsi"][:])

        # root.close()


        ds = xr.open_dataset("data/"+filename)
        df = ds.to_dataframe()

        print(df.reset_index())


if __name__ == "__main__":
    loader = DBLoader(database="weather", user='root', password='password', host="postgres_db", port=5432)
    
    loader.load("KMDS__OPER_P___10M_OBS_L2_202409222300.nc")

    