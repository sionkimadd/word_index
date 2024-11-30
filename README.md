# Wor(l)d Index

**Wor(l)d Index** is a webpage that is designed to fetch, save and analyze news.

## Milestone

1. Fetch Google news (O)
2. Save to Database (O)
3. Load data from Database (O)
4. Analyze news ( )
5. Deploy ( )

## Implementation Details

### GoogleNewsFetcher (Class)

```python
import os
from datetime import datetime, timedelta
import pandas as pd
from GoogleNews import GoogleNews
```

```python
class GoogleNewsFetcher:
```

```python
def __init__(self, search_word, days_back, output_csv):

    self.__search_word = search_word
    self.__days_back = days_back
    self.__output_csv = output_csv
```

- Initialize `GoogleNewsFetcher` with `search_word`, `days_back`, and `output_csv`.

```python
def setup_period(self):

    today = datetime.now().date()
    start_date = today - timedelta(days = self.__days_back)
    self.__start_date_str  = start_date.strftime("%m/%d/%Y")
    self.__end_date_str = today.strftime("%m/%d/%Y")
```

- `today = datetime.now().date()` get current date without time for following `GoogleNews` requirements.
- `start_date = today - timedelta(days = self.__days_back)` calculate start date by subtracting `days_back` from today's date.
- `self.__end_date_str = today.strftime("%m/%d/%Y")`, `self.__end_date_str = today.strftime("%m/%d/%Y")` format `MM/DD/YYYY` that is required by `GoogleNews`.

```python
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

```python
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
```

- `news_data = pd.DataFrame(self.__fetched_list)[["title", "datetime", "link"]]` convert a `fetched_list` (dictionaries) into a Pandas DataFrame with `title`, `datetime`, and `link` columns.
- `news_data = news_data.assign(datetime = pd.to_datetime(news_data["datetime"], errors="coerce"), search_word=self.__search_word)` convert `datetime` column to a datetime format for replacing invalid values with `NaT` and add a `search_word` column.
- `if os.path.exists(self.__output_csv):` check if CSV file already exist.
- `existing_news_data = pd.read_csv(self.__output_csv)` read the existing CSV file into a Pandas DataFrame.
- `existing_news_data["datetime"] = pd.to_datetime(existing_news_data["datetime"], errors = "coerce")` convert `datetime` column to a datetime format for replacing invalid values with `NaT`.
- `combined_news_data = pd.concat([existing_news_data, news_data], ignore_index = True)` concatenate `existing_news_data` and `news_data` into a single Pandas DataFrame without index.
- `combined_news_data.drop_duplicates(subset = ["title"], keep = "last", inplace=True)` remove duplicated news by `title` column for keeping last data.
- `combined_news_data.dropna(subset = ["datetime"], inplace=True)` remove any rows that contain `datetime` is `NaT`.
- `combined_news_data.sort_values("datetime", inplace=True)` sort the Pandas DataFrame by `datetime` in ascending order.
- `else:` else CSV file don't exist.
- `news_data.dropna(subset=["datetime"], inplace=True)` remove any rows that contain `datetime` is `NaT`.
- `combined_news_data = news_data.sort_values("datetime")` sort the Pandas DataFrame by `datetime` in ascending order.
- `combined_news_data.to_csv(self.__output_csv, index = False)` save combined and structured Pandas DataFrame to a CSV file without the index.

```python
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

### CSVtoSQL (Class)

```python
import pandas as pd
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
```

```python
class CSVtoSQL:
```

```python
def __init__(self, output_csv):

    load_dotenv()
    self.__output_csv = output_csv
    self.__table_name = "word_index"
    self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")
    self.__engine = create_engine(self.__db_url)
```

- `load_dotenv()` load the environment variables from `.env`.
- Initialize `CSVtoSQL` with `output_csv`.
- `self.__table_name = "word_index"` set the table name with `word_index`.
- `self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")` retrieve the `JAWSDB_URL` from the environment variables and reformat it to be compatible with `SQLAlchemy`.
- `self.__engine = create_engine(self.__db_url)` create a database engine to connect with the specified database.

```python
def create_table_if_not_exists(self):

    query = f"""
    CREATE TABLE IF NOT EXISTS {self.__table_name} (
        title TEXT,
        datetime TEXT,
        link TEXT,
        search_word TEXT
    );
    """
    with self.__engine.connect() as connection:
        connection.execute(text(query))
```

- `query = f"""CREATE TABLE IF NOT EXISTS {self__table_name} (title TEXT,datetime TEXT,link TEXT,search_word TEXT);"""` define a `SQL query` to create a table if not exists with `title`, `datetime`, `link`, and `search_word` columns.
- `with self.__engine.connect() as connection:connection.execute(text(query))` connect with database and execute the `SQL query` to create the table.

```python
def save_as_sql(self):

    new_data = pd.read_csv(self.__output_csv)
    existing_data = pd.read_sql(f"SELECT * FROM {self.__table_name}", self.__engine)
    combined_data = pd.concat([existing_data, new_data])
    combined_data.drop_duplicates(subset=['title'], keep = "last", inplace=True)
    combined_data.to_sql(self.__table_name, con=self.__engine, index=False, if_exists='replace')
```

- `new_data = pd.read_csv(self.__output_csv)` read CSV file into a Pandas DataFrame.
- `existing_data = pd.read_sql(f"SELECT * FROM {self.__table_name}", self.__engine)` read existing data from the database table into a Pandas DataFrame.
- `combined_data = pd.concat([existing_data, new_data])` concatenate `existing_data` and `new_data` into a single Pandas DataFrame.
- `combined_data.drop_duplicates(subset=['title'], keep = "last", inplace=True)` remove duplicated news by `title` column for keeping last data.
- `combined_data.to_sql(self.__table_name, con=self.__engine, index=False, if_exists='replace')` save combined data into database table.

```python
@property
def output_csv(self):
    return self.__output_csv

@property
def table_name(self):
    return self.__table_name

@property
def engine(self):
    return self.__engine
```

- `@property` provide read-only access to private attributes.

### SQLtoCSV (Class)

```python
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
```

```python
class SQLtoCSV:
```

```python
def __init__(self, output_sql_csv, search_word):

    load_dotenv()
    self.__output_sql_csv = output_sql_csv
    self.__search_word = search_word
    self.__table_name = "word_index"
    self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")
    self.__engine = create_engine(self.__db_url)
```

- `load_dotenv()` load the environment variables from `.env`.
- Initialize `SQLtoCSV` with `output_sql_csv` and `search_word`.
- `self.__table_name = "word_index"` set the table name with `word_index`.
- `self.__db_url = os.getenv("JAWSDB_URL").replace("mysql://", "mysql+pymysql://")` retrieve the `JAWSDB_URL` from the environment variables and reformat it to be compatible with `SQLAlchemy`.
- `self.__engine = create_engine(self.__db_url)` create a database engine to connect with the specified database.

```python
def load_to_csv(self):

    query = f"SELECT * FROM {self.__table_name} WHERE search_word = '{self.__search_word}'"
    data = pd.read_sql(query, self.__engine)
    data.to_csv(self.__output_sql_csv, index=False)
```

- `query = f"SELECT * FROM {self.__table_name} WHERE search_word = '{self.__search_word}'"` define a `SQL query` to retrieve a `word_index` that contains an only specified `search_word` column.
- `data = pd.read_sql(query, self.__engine)` read data from the database table into a Pandas DataFrame.
- `data.to_csv(self.__output_sql_csv, index=False)` save Pandas DataFrame to a CSV file without the index.

```python
@property
def output_sql_csv(self):
    return self.__output_sql_csv

@property
def table_name(self):
    return self.__table_name

@property
def search_word(self):
    return self.__search_word

@property
def engine(self):
    return self.__engine
```

- `@property` provide read-only access to private attributes.

### sortCSV (Class)

```python
import pandas as pd
```

```python
class sortCSV:
```

```python
def __init__(self, output_sql_csv):

    self.__output_sql_csv = output_sql_csv
```

- Initialize `sortCSV` with `output_sql_csv`.

```python
def sort_csv_datetime(self):

    df = pd.read_csv(self.__output_sql_csv)

    df['datetime'] = pd.to_datetime(df['datetime'])
    sorted_df = df.sort_values(by='datetime')

    sorted_df.to_csv(self.__output_sql_csv, index=False)
```

- `df = pd.read_csv(self.__output_sql_csv)` read the existing CSV file into a Pandas DataFrame.
- `df['datetime'] = pd.to_datetime(df['datetime'])` convert `datatime` column into date and time value.
- `sorted_df = df.sort_values(by='datetime')` sort Pandas DataFrame in ascending order by `datetime` column.
- `sorted_df.to_csv(self.__output_sql_csv, index=False)` save sorted Pandas DataFrame to a CSV file without the index.

```python
@property
def output_sql_csv(self):
    return self.__output_sql_csv
```

- `@property` provide read-only access to private attributes.

### SentimentAnalysis (Class)

```python
from nltk.sentiment import SentimentIntensityAnalyzer
import pandas as pd
```

```python
class SentimentAnalysis:
```

```python
def __init__(self, output_sql_csv, output_sentiment_csv):
    self.__output_sql_csv = output_sql_csv
    self.__output_sentiment_csv = output_sentiment_csv
    self.analyzer = SentimentIntensityAnalyzer()
```

- Initialize `SentimentAnalysis` with `output_sql_csv`, `output_sentiment_csv`, and `SentimentIntensityAnalyzer()`

```python
def analyze_sentiment(self):

    df = pd.read_csv(self.__output_sql_csv)

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
```

- `df = pd.read_csv(self.__output_sql_csv)` read the existing CSV file into a Pandas DataFrame.
- `sentiment_results = []` initialize with empty `list` that is for sentiment results.
- `for title in df['title']:` literate `title` from DataFrame.
- `sentiment_scores = self.analyzer.polarity_scores(title)` analyze sentiment.
- `sentiment_results.append({ 'neg': sentiment_scores['neg'], 'neu': sentiment_scores['neu'], 'pos': sentiment_scores['pos'], 'compound': sentiment_scores['compound'] })` create as a `dictionary` and append into `list`.
- `sentiment_df = pd.DataFrame(sentiment_results)` convert `sentiment_results` into a Pandas DataFrame with `neg`, `neu`, `pos`, and `compound` columns.
- `sentiment_df.to_csv(self.__output_sentiment_csv, index=False, encoding='utf-8')` save Pandas DataFrame as a `csv` without `index`.

```python
@property
def output_sql_csv(self):
    return self.__output_sql_csv

@property
def output_sentiment_csv(self):
    return self.__output_sentiment_csv
```

- `@property` provide read-only access to private attributes.

### datetimeColInserter (Class)

```python
import pandas as pd
```

```python
class datetimeColInserter:
```

```python
def __init__(self, output_sql_csv, output_sentiment_csv):
    self.__output_sql_csv = output_sql_csv
    self.__output_sentiment_csv = output_sentiment_csv
```

- Initialize `datetimeColInserter` with `output_sql_csv`, and `output_sentiment_csv`.

```python
def insert_column(self, datetime_col, compound_col, output_sentiment_csv):

    source = pd.read_csv(self.__output_sql_csv)
    target = pd.read_csv(self.__output_sentiment_csv)

    insert_position = target.columns.get_loc(compound_col) + 1
    target.insert(insert_position, datetime_col, source[datetime_col])
    target.to_csv(output_sentiment_csv, index=False)
```

- `source = pd.read_csv(self.__output_sql_csv)`, and `target = pd.read_csv(self.__output_sentiment_csv)` read `self.__output_sql_csv`, and `self.__output_sentiment_csv` into a Pandas DataFram.
- `insert_position = target.columns.get_loc(compound_col) + 1` define insert position after `compound` column in `target`.
- `target.insert(insert_position, datetime_col, source[datetime_col])` insert `source[datetime_col]` at `insert_position` as `datetime_col` name in `target`.
- `target.to_csv(output_sentiment_csv, index=False)` save `target` as `csv` without index.

```python
@property
def output_sql_csv(self):
    return self.__output_sql_csv

@property
def output_sentiment_csv(self):
    return self.__output_sentiment_csv
```

- `@property` provide read-only access to private attributes.

### compoundColInserter (Class)

```python
import pandas as pd
```

```python
class compoundColInserter:
```

```python
def __init__(self, output_sentiment_csv, output_sql_csv):

    self.__output_sentiment_csv = output_sentiment_csv
    self.__output_sql_csv = output_sql_csv
```

- Initialize `compoundColInserter` with `output_sentiment_csv`, and `output_sql_csv`.

```python
def insert_column(self, compound_col, search_word_col, output_info_csv):

    source = pd.read_csv(self.__output_sentiment_csv)
    target = pd.read_csv(self.__output_sql_csv)

    insert_position = target.columns.get_loc(search_word_col) + 1
    target.insert(insert_position, compound_col, source[compound_col])
    target.to_csv(output_info_csv, index=False)
```

- `source = pd.read_csv(self.__output_sentiment_csv)`, and `target = pd.read_csv(self.__output_sql_csv)` read `self.__output_sentiment_csv`, and `self.__output_sql_csv` into a Pandas DataFram.
- `insert_position = target.columns.get_loc(search_word_col) + 1` define insert position after `search_word` column in `target`.
- `target.insert(insert_position, compound_col, source[compound_col])` insert `source[compound_col]` at `insert_position` as `compound_col` name in `target`.
- `target.to_csv(output_info_csv, index=False)` save `target` as `csv` without index.

```python
@property
def output_sentiment_csv(self):
    return self.__output_sentiment_csv

@property
def output_sql_csv(self):
    return self.__output_sql_csv
```

- `@property` provide read-only access to private attributes.

### ??? (Class)
