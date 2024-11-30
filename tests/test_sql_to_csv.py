"""
python -m unittest tests/test_sql_to_csv.py
"""
import unittest
import pandas as pd
from sql_to_csv.sql_to_csv import SQLtoCSV

class TestSQLtoCSV(unittest.TestCase):

    def test_init_valid(self):
        csv_to_sql = SQLtoCSV("nasdaq.csv", "nasdaq")
        self.assertEqual("nasdaq.csv", csv_to_sql.output_sql_csv)
        self.assertEqual("nasdaq", csv_to_sql.search_word)

    def setUp(self):
        self.test_output_sql_csv = "kimsion_sql.csv"
        self.test_search_word = "kimsion"
        self.csv_to_sql = SQLtoCSV(self.test_output_sql_csv, self.test_search_word)

    def test_load_to_csv(self):
        self.csv_to_sql.load_to_csv()
        sql_df = pd.read_csv(self.test_output_sql_csv)
        expected_df = pd.DataFrame({
            "title": ["Happy Test 1", "Sad Test 2", "Angry Test 3"],
            "datetime": ["2000-08-30", "1999-08-30", "1998-08-30"],
            "link": ["http://example.com/", "http://example.com/", "http://example.com/"],
            "search_word": ["kimsion", "kimsion", "kimsion"]
        })
        pd.testing.assert_frame_equal(sql_df, expected_df)