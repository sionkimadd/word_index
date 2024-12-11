import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv

class SQLtoCSV:

    def __init__(self, output_sql_csv, search_word):

        load_dotenv()
        self.__output_sql_csv = output_sql_csv
        self.__search_word = search_word
        self.__table_name = "word_index"
        self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")
        self.__engine = create_engine(self.__db_url)
        
    def load_to_csv(self):

        query = f"SELECT * FROM {self.__table_name} WHERE search_word = '{self.__search_word}'"
        data = pd.read_sql(query, self.__engine)
        data.to_csv(self.__output_sql_csv, index=False)

    @property
    def output_sql_csv(self):
        return self.__output_sql_csv

    @property
    def table_name(self):
        return self.__table_name
    
    @property
    def search_word(self):
        return self.__search_word

    @property
    def engine(self):
        return self.__engine