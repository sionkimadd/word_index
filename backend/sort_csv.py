import pandas as pd

class sortCSV:

    def __init__(self, output_sql_csv):
        
        self.__output_sql_csv = output_sql_csv
    
    def sort_csv_datetime(self):

        df = pd.read_csv(self.__output_sql_csv)

        df['datetime'] = pd.to_datetime(df['datetime'])
        sorted_df = df.sort_values(by='datetime')

        sorted_df.to_csv(self.__output_sql_csv, index=False)

    @property
    def output_sql_csv(self):
        return self.__output_sql_csv