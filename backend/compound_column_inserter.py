import pandas as pd

class compoundColInserter:
    
    def __init__(self, output_sentiment_csv, output_sql_csv):
        
        self.__output_sentiment_csv = output_sentiment_csv
        self.__output_sql_csv = output_sql_csv

    def insert_column(self, compound_col, search_word_col, output_info_csv):

        source = pd.read_csv(self.__output_sentiment_csv)
        target = pd.read_csv(self.__output_sql_csv)

        insert_position = target.columns.get_loc(search_word_col) + 1
        target.insert(insert_position, compound_col, source[compound_col])
        target.to_csv(output_info_csv, index=False)

    @property
    def output_sentiment_csv(self):
        return self.__output_sentiment_csv
    
    @property
    def output_sql_csv(self):
        return self.__output_sql_csv