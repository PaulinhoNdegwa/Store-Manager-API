from app.tests.v2.basetest import BaseTest
from flask import json


class UsersTestCase(BaseTest):
    """Test suite for users"""

    def test_get_all_users(self):
        """Test retrueval of all users"""
        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users", headers=dict(Authorization = "Bearer "+access_token))
        self.assertIsInstance(json.loads(response.data), list)

    def test_get_one_user(self):
        """Test get one user"""
        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users/1", headers=dict(Authorization = "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 200)