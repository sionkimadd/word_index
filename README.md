# Wor(l)d Index

**Wor(l)d Index** is a webpage that is designed to fetch, save and analyze news.

## Milestone

1. Fetch Google news (O)
2. Save to Database ( )
3. Analyze news ( )
4. Deploy ( )

## Implementation Details

### GoogleNewsFetcher (Class)
```javascript
import os
from datetime import datetime, timedelta
import pandas as pd
from GoogleNews import GoogleNews
```
```javascript
class GoogleNewsFetcher:
```
```javascript
def __init__(self, search_word, days_back, output_csv):
    
    self.__search_word = search_word
    self.__days_back = days_back
    self.__output_csv = output_csv
```
- Initialize GoogleNewsFetcher with `search_word`, `days_back`, and `output_csv`.

```javascript
def setup_period(self):

    today = datetime.now().date()
    start_date = today - timedelta(days = self.__days_back)
    self.__start_date_str  = start_date.strftime("%m/%d/%Y")
    self.__end_date_str = today.strftime("%m/%d/%Y")
```
- `today = datetime.now().date()` get current date without time for following `GoogleNews` requirements.
- `start_date = today - timedelta(days = self.__days_back)` calculate start date by subtracting `days_back` from today's date.
- `self.__end_date_str = today.strftime("%m/%d/%Y")`, `self.__end_date_str = today.strftime("%m/%d/%Y")` format `MM/DD/YYYY` that is required by `GoogleNews`.

```javascript
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
```
- `g_news = GoogleNews(start = self.__start_date_str , end = self.__end_date_str)` initialize `GoogleNews` with the specified date range.
- `g_news.get_news(self.__search_word)` fetch news with a specific `search_word`.
- `self.__fetched_list = g_news.results()` save fetched news as a list.
- `if not self.__fetched_list: raise Exception(f"Error for {self.__search_word}.")` raise `Exception` with a message.
- `return self.__fetched_list` return fetched news list.

```javascript
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
        combined_news_data = combined_news_data.drop_duplicates(subset = ["title"], keep = "last")
        combined_news_data = combined_news_data.dropna(subset = ["datetime"])
        combined_news_data = combined_news_data.sort_values("datetime")
    
    else:
        news_data = news_data.dropna(subset=["datetime"])
        combined_news_data = news_data.sort_values("datetime")

    combined_news_data.to_csv(self.__output_csv, index = False)
```
- `news_data = pd.DataFrame(self.__fetched_list)[["title", "datetime", "link"]]` convert a `fetched_list` (dictionaries) into a Pandas DataFrame with `title`, `datetime`, and `link` columns.
- `news_data = news_data.assign(datetime = pd.to_datetime(news_data["datetime"], errors="coerce"), search_word=self.__search_word)` convert `datetime` column to a datetime format for replacing invalid values with `NaT` and add a `search_word` column.
- `if os.path.exists(self.__output_csv):` check if CSV file already exist.
- `existing_news_data = pd.read_csv(self.__output_csv)` read the existing CSV file into a Pandas DataFrame.
- `existing_news_data["datetime"] = pd.to_datetime(existing_news_data["datetime"], errors = "coerce")` convert `datetime` column to a datetime format for replacing invalid values with `NaT`.
- `combined_news_data = pd.concat([existing_news_data, news_data], ignore_index = True)` concatenate `existing_news_data` and `news_data` into a single Pandas DataFrame without index.
- `combined_news_data = combined_news_data.drop_duplicates(subset = ["title"], keep = "last")` remove duplicated news by `title` column for keeping last data.
- `combined_news_data = combined_news_data.dropna(subset = ["datetime"])` remove any rows that contain `datetime` is `NaT`.
- `combined_news_data = combined_news_data.sort_values("datetime")` sort the Pandas DataFrame by `datetime` in ascending order.
- `else:` else CSV file don't exist.
- `news_data = news_data.dropna(subset=["datetime"])` remove any rows that contain `datetime` is `NaT`.
- `combined_news_data = news_data.sort_values("datetime")` sort the Pandas DataFrame by `datetime` in ascending order.
- `combined_news_data.to_csv(self.__output_csv, index = False)` save combined and structured Pandas DataFrame to a CSV file without the index.

```javascript
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
```
- `@property` provide read-only access to private attributes.

### ??? (Class)