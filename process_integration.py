from csv_to_sql.csv_to_sql import CSVtoSQL
from google_news_fetcher.google_news_fetcher import GoogleNewsFetcher

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