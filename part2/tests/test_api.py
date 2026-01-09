import unittest
import json
from app.main import app

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_health(self):
        res = self.client.get('/api/v1/health/')
        self.assertEqual(res.status_code, 200)
