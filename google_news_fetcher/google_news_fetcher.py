import os
from datetime import datetime, timedelta
import pandas as pd
from GoogleNews import GoogleNews

class GoogleNewsFetcher:
    
    def __init__(self, search_word, days_back, output_csv):
        
        self.__search_word = search_word
        self.__days_back = days_back
        self.__output_csv = output_csv

    def setup_period(self):

        today = datetime.now().date()
        start_date = today - timedelta(days = self.__days_back)
        self.__start_date_str  = start_date.strftime("%m/%d/%Y")
        self.__end_date_str = today.strftime("%m/%d/%Y") 

    def fetch_news(self):

        try:
            g_news = GoogleNews(start = self.__start_date_str , end = self.__end_date_str)
            g_news.get_news(self.__search_word)
            self.__fetched_list = g_news.results()

            if not self.__fetched_list:
                raise Exception(f"Error for {self.__search_word}.")
        
        except Exception as e:
            raise e
        
        return self.__fetched_list
    
    def save_as_csv(self):

        news_data = pd.DataFrame(self.__fetched_list)[["title", "datetime", "link"]]
        news_data = news_data.assign(
            datetime = pd.to_datetime(news_data["datetime"], errors="coerce"),
            search_word = self.__search_word
        )

        if os.path.exists(self.__output_csv):
            existing_news_data = pd.read_csv(self.__output_csv)
            existing_news_data["datetime"] = pd.to_datetime(existing_news_data["datetime"], errors = "coerce")
            combined_news_data = pd.concat([existing_news_data, news_data], ignore_index = True)
            combined_news_data.drop_duplicates(subset = ["title"], keep = "last", inplace=True)
            combined_news_data.dropna(subset = ["datetime"], inplace=True)
            combined_news_data.sort_values("datetime", inplace=True)
        
        else:
            news_data.dropna(subset=["datetime"], inplace=True)
            combined_news_data = news_data.sort_values("datetime")

        combined_news_data.to_csv(self.__output_csv, index = False)

    @property
    def search_word(self):
        return self.__search_word

    @property
    def days_back(self):
        return self.__days_back

    @property
    def output_csv(self):
        return self.__output_csv

    @property
    def start_date_str(self):
        return self.__start_date_str

    @property
    def end_date_str(self):
        return self.__end_date_str

    @property
    def fetched_list(self):
        return self.__fetched_list