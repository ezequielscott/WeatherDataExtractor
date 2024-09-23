import logging
import xarray as xr
from sqlalchemy import create_engine
import datetime

class DataLoader:

    def __init__(self, database: str, user: str, password: str, host: str, port: int):
        """Class constructor

        Args:
            database (str): name of the database
            user (str): user to connect to the database
            password (str): password for the user database
            host (str): host name of the database
            port (int): port of the database
        """
        
        # initialize the log
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("logs/debug.log", mode="w"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)

        self.logger.info(f"Connecting to database...")
        try:
            self.engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")
            self.logger.info(f"Connection OK.")
        except:
            self.logger.error(f"ERROR connecting to database.")

    
    def load(self, filename: str, tablename: str):
        """Main method to load the contents of a filename into the database.
        
        This method converts the filename into a pandas dataframe, 
        it adds a new field `updated_at`, and save it to the database.
        The records are appended to the table.

        Args:
            filename (str): filename to save into the database.
            tablename (str): table where the records are saved to.
        """

        # root = Dataset("data/"+filename, "r", format="NETCDF4")
        # logging.info("DIMENSIONS:")
        # logging.info(root.dimensions.values())

        # print([d for d in root.dimensions.values()])

        # logging.info("VARIABLES:")
        # logging.info(root.variables.keys())

        # print(root.variables["wsi"][:])

        # root.close()

        ds = xr.open_dataset("data/"+filename)
        
        self.logger.info("Transforming dataset...")
        df = ds.to_dataframe()
        self.logger.info("Transformation OK.")
        
        self.logger.info("Saving to database...")
        df['updated_at'] = datetime.datetime.now()
        df.to_sql(name=tablename, con=self.engine, if_exists='append')
        self.logger.info("Saving OK.")
