import os
import unittest
import json
from app import create_app, db
from config import TestConfig
from app.models import TimeLine


class ApiTest(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)
        self.db_url = TestConfig.SQLALCHEMY_DATABASE_URI
        self.api_headers = {'Accept': 'application/json',
                            'Content-Type': 'application/json'}
        obj = TimeLine(asin='B0014D3N0Q', brand='Downy', id='R11QPQWAH45REP',
                            source='amazon', stars=5, timestamp=1548799200)
        db.session.add(obj)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_404(self):
        res = self.client.get('invalid/url', headers=self.api_headers)
        self.assertTrue(res.status_code == 404)

    def test_info(self):
        res = self.client.get('api/info', headers=self.api_headers)
        self.assertTrue(res.status_code == 200)
        json_res = json.loads(res.data)

        self.assertIn('brand', json_res)
        self.assertEqual(type(json_res['brand']), type([]))
        self.assertIn('asin', json_res)
        self.assertEqual(type(json_res['asin']), type([]))
        self.assertIn('stars', json_res)
        self.assertEqual(type(json_res['stars']), type([]))
        self.assertIn('source', json_res)
        self.assertEqual(type(json_res['brand']), type([]))

    def test_timeline(self):

        res = self.client.get('api/timeline', headers=self.api_headers)
        json_res = json.loads(res.data)
        self.assertTrue(res.status_code == 200)
        self.assertEqual(json_res['massage'], 'Missing params')

        res = self.client.get('/api/timeline?startDate=2019-01-01&endDate=2020-01-01&Type=cumulative&Grouping=weekly')
        json_res = json.loads(res.data)
        self.assertIn('timeline', json_res)
