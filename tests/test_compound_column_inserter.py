"""
python -m unittest tests/test_compound_column_inserter.py
"""
import unittest
import pandas as pd
from backend.compound_column_inserter import compoundColInserter

class TestcompoundColInserter(unittest.TestCase):

    def test_init_valid(self):

        datetime_inserter = compoundColInserter("nasdaq_sentiment.csv", "nasdaq_sql.csv")
        self.assertEqual("nasdaq_sentiment.csv", datetime_inserter.output_sentiment_csv)
        self.assertEqual( "nasdaq_sql.csv", datetime_inserter.output_sql_csv)

    def setUp(self):
        self.output_sentiment_csv = "kimsion_sentiment.csv"
        self.output_sql_csv = "kimsion_sql.csv"
        self.info_senti_merger = compoundColInserter(self.output_sentiment_csv, self.output_sql_csv)

    def test_insert_column(self):

        self.output_sql_csv = self.output_sql_csv.replace('sql.csv', 'info.csv')
        self.info_senti_merger.insert_column("compound", "search_word", "kimsion_info.csv")
        df = pd.read_csv(self.output_sql_csv)
        header = df.columns.tolist()
        expected_header = ['title', 'datetime', 'link', 'search_word', 'compound']
        self.assertEqual(header, expected_header)