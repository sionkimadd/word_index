from backend import *

def fetch_google_news(search_word, days_back):
    output_csv = f"{search_word}.csv"
    news_fetcher = GoogleNewsFetcher(search_word, days_back, output_csv)
    news_fetcher.setup_period()
    news_fetcher.fetch_news()
    news_fetcher.save_as_csv()
    return output_csv

def save_database(output_csv):
    csv_to_sql = CSVtoSQL(output_csv)
    csv_to_sql.create_table_if_not_exists()
    csv_to_sql.save_as_sql()

def database_to_csv(search_word):
    output_sql_csv = f"{search_word}_sql.csv"
    sql_to_csv = SQLtoCSV(output_sql_csv, search_word)
    sql_to_csv.load_to_csv()
    return output_sql_csv

def sort_csv_by_datetime(output_sql_csv):
    sort_csv = sortCSV(output_sql_csv)
    sort_csv.sort_csv_datetime()
    return output_sql_csv

def analyze_sentiment_nltk(output_sql_csv):
    output_sentiment_csv = output_sql_csv.replace('sql.csv', 'sentiment.csv')
    sentiment_analysis = SentimentAnalysis(output_sql_csv, output_sentiment_csv)
    sentiment_analysis.analyze_sentiment()
    return output_sentiment_csv

def insert_datetime(output_sql_csv, output_sentiment_csv):
    datetime_insert = datetimeColInserter(output_sql_csv, output_sentiment_csv)
    datetime_insert.insert_column('datetime', 'compound', output_sentiment_csv)
    return output_sentiment_csv

def insert_compound(output_sentiment_csv, output_sql_csv):
    output_info_csv = output_sql_csv.replace('sql.csv', 'info.csv')
    datetime_insert = datetimeColInserter(output_sentiment_csv, output_sql_csv)
    datetime_insert.insert_column('compound', 'search_word', output_info_csv)
    return output_info_csv

def plotter_sentiment_nltk(search_word, output_sentiment_csv):
    plotter = SentimentPlotter(output_sentiment_csv)
    plotter.plot_sentiment(search_word)