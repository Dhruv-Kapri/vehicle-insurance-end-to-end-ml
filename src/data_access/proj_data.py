import sys
from typing import Optional

import numpy as np
import pandas as pd

from src.configuration import MongoDBClient
from src.constants import DATABASE_NAME
from src.exception import MyException
from src.logger import logger


class Proj_Data:
    """
    A class to export MongoDB records as a pandas DataFrame.
    """

    def __init__(self) -> None:
        try:
            self.mongo_client = MongoDBClient(database_name=DATABASE_NAME)
        except Exception as e:
            raise MyException(e, sys)

    def export_collection_as_dataframe(
        self, collection_name: str, database_name: Optional[str] = None
    ) -> pd.DataFrame:
        """
        Exports an entire MongoDB collection as a pandas DataFrame.

        Parameters:
        ----------
        collection_name : str
            The name of the MongoDB collection to export.
        database_name : Optional[str]
            Name of the database (optional). Defaults to DATABASE_NAME.

        Returns:
        -------
        pd.DataFrame
            DataFrame containing the collection data, with '_id' column removed and 'na' values replaced with NaN.
        """
        try:
            # Access specified collection from the default or specified database
            if database_name is None:
                collection = self.mongo_client.database[collection_name]
            else:
                collection = self.mongo_client.client[database_name][collection_name]

            # Convert collection data to DataFrame and preprocess
            logger.info("Fetching data from MongoDB")
            df = pd.DataFrame(list(collection.find()))
            logger.info(f"Data fetched: {len(df)} records")

            columns_to_drop = ["_id", "id"]
            df = df.drop(columns=[col for col in columns_to_drop if col in df.columns])
            df.replace({"na": np.nan}, inplace=True)
            return df

        except Exception as e:
            raise MyException(e, sys)
