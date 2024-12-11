"""
python -m unittest tests/test_datetime_column_inserter.py
"""
import unittest
import pandas as pd
from backend.datetime_column_inserter import datetimeColInserter

class TestdatetimeColInserter(unittest.TestCase):

    def test_init_valid(self):

        datetime_inserter = datetimeColInserter("nasdaq_sql.csv", "nasdaq_sentiment.csv")
        self.assertEqual("nasdaq_sql.csv", datetime_inserter.output_sql_csv)
        self.assertEqual( "nasdaq_sentiment.csv", datetime_inserter.output_sentiment_csv)

    def setUp(self):
        self.output_sql_csv = "kimsion_sql.csv"
        self.output_sentiment_csv = "kimsion_sentiment.csv"
        self.datetime_col_inseter = datetimeColInserter(self.output_sql_csv, self.output_sentiment_csv)

    def test_insert_column(self):

        self.datetime_col_inseter.insert_column("datetime", "compound", "kimsion_sentiment.csv")
        df = pd.read_csv(self.output_sentiment_csv)
        header = df.columns.tolist()
        expected_header = ['neg', 'neu', 'pos', 'compound', 'datetime']
        self.assertEqual(header, expected_header)