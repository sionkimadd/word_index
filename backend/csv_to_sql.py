import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

class CSVtoSQL:

    def __init__(self, output_csv):

        load_dotenv()
        self.__output_csv = output_csv
        self.__table_name = "word_index"
        self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")
        self.__engine = create_engine(self.__db_url)

    def create_table_if_not_exists(self):

        query = f"""
        CREATE TABLE IF NOT EXISTS {self.__table_name} (
            title TEXT,
            datetime TEXT,
            link TEXT,
            search_word TEXT
        );
        """
        with self.__engine.connect() as connection:
            connection.execute(text(query))

    def save_as_sql(self):

        new_data = pd.read_csv(self.__output_csv)
        existing_data = pd.read_sql(f"SELECT * FROM {self.__table_name}", self.__engine)
        combined_data = pd.concat([existing_data, new_data])
        combined_data.drop_duplicates(subset=['title'], keep = "last", inplace=True)
        combined_data.to_sql(self.__table_name, con=self.__engine, index=False, if_exists='replace')

    @property
    def output_csv(self):
        return self.__output_csv

    @property
    def table_name(self):
        return self.__table_name

    @property
    def engine(self):
        return self.__engine