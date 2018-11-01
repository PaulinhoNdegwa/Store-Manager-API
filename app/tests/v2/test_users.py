from app.tests.v2.basetest import BaseTest
from flask import json
from .data import new_role


class UsersTestCase(BaseTest):
    """Test suite for users"""

    def test_get_all_users(self):
        """Test retrieval of all users"""

        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertIsInstance(json.loads(response.data)["Users"], list)

    def test_get_one_user(self):
        """Test get one user"""

        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users/1",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)

    def test_get_inexistent_user(self):
        """Test get inexistent user"""

        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users/10",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)

    def test_get_users_as_attendant(self):
        """Test get users as attendant"""

        access_token = self.authenticate()
        response = self.client.get("/api/v2/users",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 401)

    def test_get_nonint_user_id(self):
        """Test get user using a nonint user_id"""

        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/users/qw",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)

    def test_update_user_role(self):
        """This method tests the update of user role"""

        access_token = self.authenticateAdmin()
        self.authenticate()
        response = self.client.put("/api/v2/users/2",
                                   data=json.dumps(new_role),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)

    def test_update_role_as_attendant(self):
        """This method tests the update of user role"""

        access_token = self.authenticate()
        response = self.client.put("/api/v2/users/2",
                                   data=json.dumps(new_role),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 401)
