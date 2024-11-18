"""
python -m unittest tests/test_csv_to_sql.py
"""
import unittest
import pandas as pd
from csv_to_sql.csv_to_sql import CSVtoSQL
from sqlalchemy import text

class TestCSVtoSQL(unittest.TestCase):

    def test_init_valid(self):
        csv_to_sql = CSVtoSQL("nasdaq.csv")
        self.assertEqual("nasdaq.csv", csv_to_sql.output_csv)
        
    def setUp(self):
        self.test_csv = "test_data.csv"
        self.test_data = pd.DataFrame({
            "title": ["Test 1", "Test 2", "Test 3"],
            "datetime": ["2000-08-30", "1999-08-30", "1998-08-30"],
            "link": ["http://example.com/", "http://example.com/", "http://example.com/"],
            "search_word": ["kimsion", "kimsion", "kimsion"]
        })
        self.test_data.to_csv(self.test_csv, index=False)
        self.csv_to_sql = CSVtoSQL(self.test_csv)

    def test_create_table_if_not_exists(self):
        self.csv_to_sql.create_table_if_not_exists()
        with self.csv_to_sql.engine.connect() as connection:
            tables = [table[0] for table in connection.execute(text("SHOW TABLES;"))]
        self.assertIn("word_index", tables)

    def test_save_as_sql(self):
        self.csv_to_sql.create_table_if_not_exists()
        self.csv_to_sql.save_as_sql()
        with self.csv_to_sql.engine.connect() as connection:
            db_data = pd.read_sql_table(self.csv_to_sql.table_name, connection)
        self.assertListEqual(list(db_data.columns), list(self.test_data.columns))