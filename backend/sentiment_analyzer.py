from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd

class SentimentAnalysis:
    
    def __init__(self, output_sql_csv, output_sentiment_csv):
        self.__output_sql_csv = output_sql_csv
        self.__output_sentiment_csv = output_sentiment_csv
        self.analyzer = SentimentIntensityAnalyzer()

    def analyze_sentiment(self):

        df = pd.read_csv(self.__output_sql_csv)

        df['title'] = df['title'].fillna("")

        sentiment_results = []

        for title in df['title']:
            
            sentiment_scores = self.analyzer.polarity_scores(title)
            
            sentiment_results.append({
                'neg': sentiment_scores['neg'],
                'neu': sentiment_scores['neu'],
                'pos': sentiment_scores['pos'],
                'compound': sentiment_scores['compound']
            })

        sentiment_df = pd.DataFrame(sentiment_results)

        sentiment_df.to_csv(self.__output_sentiment_csv, index=False, encoding='utf-8')

    @property
    def output_sql_csv(self):
        return self.__output_sql_csv
    
    @property
    def output_sentiment_csv(self):
        return self.__output_sentiment_csv
