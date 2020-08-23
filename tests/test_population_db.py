import os
import unittest
import csv
from app import create_app, db
from populate_db import populate_db_csv
from config import TestConfig
from sqlalchemy.exc import OperationalError
from pandas.errors import ParserError


def create_test_csv():

    fieldnames = ['asin', 'brand', 'id', 'source', 'stars', 'timestamp']

    with open('test.csv', 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow({'asin': 'B0014D3N0Q', 'brand': 'Downy',
                         'id': 'R11QPQWAH45REP', 'source': 'amazon',
                         'stars': 5, 'timestamp': 1548799200})


class PopulationDBTests(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        self.db_url = TestConfig.SQLALCHEMY_DATABASE_URI
        create_test_csv()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
        os.remove('test.csv')
        os.remove('test.sqlite')

    def test_populate_with_valid_file_name(self):
        """Check valid population db"""
        self.assertIsNone(populate_db_csv('test.csv', self.db_url))

    def test_populate_with_invalid_file_name(self):
        """Check population db with invalid csv file name"""

        with self.assertRaises(FileNotFoundError):
            populate_db_csv('invalid_file.csv', self.db_url)

    def test_populate_with_invalid_csv_file(self):
        """Check population db with invalid csv file """

        fieldnames = ['invalid', 'brand', 'id', 'source', 'stars', 'timestamp']
        with open('invalid.csv', 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerow({'invalid': 'B0014D3N0Q', 'brand': 'Downy',
                             'id': 'R11QPQWAH45REP', 'source': 'amazon',
                             'stars': '5', 'timestamp': '1548799200'})
        with self.assertRaises(OperationalError):
            populate_db_csv('invalid.csv', self.db_url)
        os.remove('invalid.csv')

    def test_populate_with_no_csv_file(self):
        """Check population db without csv file """

        with self.assertRaises(ParserError):
            populate_db_csv('manage.py', self.db_url)
