import pandas as pd

class datetimeColInserter:
    
    def __init__(self, output_sql_csv, output_sentiment_csv):
        self.__output_sql_csv = output_sql_csv
        self.__output_sentiment_csv = output_sentiment_csv

    def insert_column(self, datetime_col, compound_col, output_sentiment_csv):

        source = pd.read_csv(self.__output_sql_csv)
        target = pd.read_csv(self.__output_sentiment_csv)

        insert_position = target.columns.get_loc(compound_col) + 1
        target.insert(insert_position, datetime_col, source[datetime_col])
        target.to_csv(output_sentiment_csv, index=False)

    @property
    def output_sql_csv(self):
        return self.__output_sql_csv
    
    @property
    def output_sentiment_csv(self):
        return self.__output_sentiment_csv