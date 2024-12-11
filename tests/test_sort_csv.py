"""
python -m unittest tests/test_sort_csv.py
"""
import unittest
import pandas as pd
from backend.sort_csv import sortCSV

class TestsortCSV(unittest.TestCase):

    def test_init_valid(self):
        sort_csv = sortCSV("nasdaq.csv")
        self.assertEqual("nasdaq.csv", sort_csv.output_sql_csv)

    def setUp(self):
        self.test_output_sql_csv = "kimsion_sql.csv"
        self.sort_csv = sortCSV(self.test_output_sql_csv)

    def test_sort_csv_datetime(self):
        self.sort_csv.sort_csv_datetime()
        sorted_df = pd.read_csv(self.test_output_sql_csv)
        expected_df = pd.DataFrame({
            "title": ["Angry Test 3", "Sad Test 2", "Happy Test 1"],
            "datetime": ["1998-08-30", "1999-08-30", "2000-08-30"],
            "link": ["http://example.com/", "http://example.com/", "http://example.com/"],
            "search_word": ["kimsion", "kimsion", "kimsion"]
        })
        pd.testing.assert_frame_equal(sorted_df, expected_df)