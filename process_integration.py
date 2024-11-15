from google_news_fetcher.google_news_fetcher import GoogleNewsFetcher

def fetch_google_news(search_word, days_back):
    output_csv = f"{search_word}.csv"
    news_fetcher = GoogleNewsFetcher(search_word, days_back, output_csv)
    news_fetcher.setup_period()
    news_fetcher.fetch_news()
    news_fetcher.save_as_csv()
    return output_csv