# Weather Data Extractor
A solution to extract weather data from public sources.

## Solution

This is a simple solution developed fully in Python.

The following diagram shows the main components used to build a data pipeline that extracts data from KNMI sources and saves the data to a database.

https://developer.dataplatform.knmi.nl/apis/

![image](design.drawio.png)

### Design decisions

* The schedule must be every 10 minutes since the weather stations report every 10 minutes. See https://dataplatform.knmi.nl/dataset/actuele10mindataknmistations-2
* Airflow allows for easy set-up and monitoring of DAGs written in Python.
* The class `WeatherDataExtractor` (`extractor.py`) is created for data extraction tasks. This class manages the connection, api keys provisions, and also saves the raw dataset in a folder for backup purposes.
* The class `DataLoader` (`loader.py`) manages the load step. It is in charge of stablishing the connection to the database and saving the file contents to a table in the dataase.
* Currently, the `DataLoader` includes a transformation step. The simple transformation includes reading the `.nc` file and converting it into a pandas dataframe. This dataframe is used for saving into the database. As future work, this step should be extracted into a new class to have a better separation of concerns. 
