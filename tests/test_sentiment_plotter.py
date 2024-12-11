"""
python -m unittest tests/test_sentiment_plotter.py
"""
import os
import unittest
from backend.sentiment_plotter import SentimentPlotter

class TestSentimentPlotter(unittest.TestCase):

    def tearDown(self):
        if os.path.exists("static/png/sentiment_plot_kimsion.png"):
            os.remove("static/png/sentiment_plot_kimsion.png")

    def test_init_valid(self):
        sentiment_plotter = SentimentPlotter("kimsion_sentiment.csv")
        self.assertEqual("kimsion_sentiment.csv", sentiment_plotter.output_sentiment_csv)

    def setUp(self):
        self.output_sentiment_csv = "kimsion_sentiment.csv"
        self.sentiment_plotter = SentimentPlotter(self.output_sentiment_csv)

    def test_plot_sentiment(self):
        self.sentiment_plotter.plot_sentiment("kimsion")
        plot_filepath = "static/png/sentiment_plot_kimsion.png"
        self.assertTrue(os.path.exists(plot_filepath))