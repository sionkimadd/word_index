"""
python -m unittest tests/test_google_news_fetcher.py
"""
import unittest
from backend.google_news_fetcher import GoogleNewsFetcher
from datetime import datetime, timedelta
import pandas as pd
import os

class TestGoogleNewsFetcher(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("nasdaq.csv"):
            os.remove("nasdaq.csv")

    def test_init_valid(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", 7, "nasdaq.csv")
        self.assertEqual("nasdaq", google_news_fetcher.search_word)
        self.assertEqual(7, google_news_fetcher.days_back)
        self.assertEqual("nasdaq.csv", google_news_fetcher.output_csv)

    def test_init_empty_search_word(self):
        google_news_fetcher = GoogleNewsFetcher(" ", 7, "nasdaq.csv")
        self.assertEqual(google_news_fetcher.search_word, " ")

    def test_init_empty_days_back(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", " ", "nasdaq.csv")
        self.assertEqual(google_news_fetcher.days_back, " ")

    def test_init_empty_csv_file(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", 7, " ")
        self.assertEqual(google_news_fetcher.output_csv, " ")

    def test_setup_period(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", 7, None)
        google_news_fetcher.setup_period()
        today = datetime.now().date()
        start_date = today - timedelta(days=7)
        self.assertEqual(google_news_fetcher.start_date_str, start_date.strftime("%m/%d/%Y"))
        self.assertEqual(google_news_fetcher.end_date_str, today.strftime("%m/%d/%Y"))

    def test_fetch_news(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", 7, None)
        google_news_fetcher.setup_period()
        google_news_fetcher.fetch_news()
        self.assertIsNotNone(google_news_fetcher.fetched_list)
        self.assertIsInstance(google_news_fetcher.fetched_list, list)
        self.assertGreater(len(google_news_fetcher.fetched_list), 0)

    def test_invalid_searchword_fetch_news(self):
        google_news_fetcher = GoogleNewsFetcher("Invalid_Search_Word", 7, None)
        google_news_fetcher.setup_period()
        with self.assertRaises(Exception) as context:
            google_news_fetcher.fetch_news()
        self.assertEqual(str(context.exception), "Error for Invalid_Search_Word.")

    def test_invalid_days_back_fetch_news(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", -7, None)
        google_news_fetcher.setup_period()
        with self.assertRaises(Exception) as context:
            google_news_fetcher.fetch_news()
        self.assertEqual(str(context.exception), "Error for nasdaq.")

    def test_save_as_csv(self):
        google_news_fetcher = GoogleNewsFetcher("nasdaq", 7, "nasdaq.csv")
        google_news_fetcher.setup_period()
        google_news_fetcher.fetch_news()
        google_news_fetcher.save_as_csv()
        csv_data = pd.read_csv("nasdaq.csv")
        self.assertIn("title", csv_data.columns)
        self.assertIn("datetime", csv_data.columns)
        self.assertIn("link", csv_data.columns)
        self.assertIn("search_word", csv_data.columns)
        self.assertGreater(len(csv_data), 0)
        self.assertTrue((csv_data["search_word"] == "nasdaq").all())