"""
python -m unittest tests/test_sentiment_analyzer.py
"""
import unittest
import pandas as pd
from sentiment_analyzer.sentiment_analyzer import SentimentAnalysis

class TestSentimentAnalysis(unittest.TestCase):

    def test_init_valid(self):
        sentiment_analysis = SentimentAnalysis("nasdaq.csv", "nasdaq_scores.csv")
        self.assertEqual("nasdaq.csv", sentiment_analysis.output_sql_csv)
        self.assertEqual("nasdaq_scores.csv", sentiment_analysis.output_sentiment_csv)

    def setUp(self):
        self.output_sql_csv = "kimsion_sql.csv"
        self.output_sentiment_csv = "kimsion_sentiment.csv"
        self.sentiment_analysis = SentimentAnalysis(self.output_sql_csv, self.output_sentiment_csv)

    def test_analyze_sentiment(self):

        self.sentiment_analysis.analyze_sentiment()
        df = pd.read_csv(self.output_sentiment_csv)
        header = df.columns.tolist()
        expected_header = ['neg', 'neu', 'pos', 'compound']
        self.assertEqual(header, expected_header)