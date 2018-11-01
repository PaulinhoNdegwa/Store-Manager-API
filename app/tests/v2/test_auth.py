from app.tests.v2.basetest import BaseTest
from flask import json
import pytest_timeout
import pytest
from .data import (admin_login, signup_details, login_details,
                   invalid_email, header_with_token, header_without_token)


class AuthTestCase(BaseTest):
    """Authentication test suite"""

    @pytest.mark.timeout(30)
    def test_successful_signup(self):
        """Function to test successful signup"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/auth/signup",
                                    data=json.dumps(signup_details),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 201)

    @pytest.mark.timeout(30)
    def test_signup_with_invalid_email(self):
        """Function to test  signup with invalid email"""

        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/auth/signup",
                                    data=json.dumps(invalid_email),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 400)

    @pytest.mark.timeout(30)
    def test_login_with_invalid_password(self):
        """Function to test login with invalid password"""
        user = {
            "email": "paul@email.com",
            "password": "123456"
        }
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        self.client.post("/api/v2/auth/signup",
                         data=json.dumps(signup_details),
                         headers=header_without_token)
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(user),
                                    headers=header_without_token)
        self.assertEqual(json.loads(response.data)["status"], 400)

    @pytest.mark.timeout(30)
    def test_successful_login(self):
        """Function to test successful login"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/signup", data=json.dumps(signup_details),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/auth/login",
                                    data=json.dumps(login_details),
                                    headers=header_without_token)
        self.assertEqual(json.loads(response.data)["status"], 200)

    @pytest.mark.timeout(30)
    def test_signout(self):
        """This method tests logout"""
        access_token = self.authenticateAdmin()
        res = self.client.put("/api/v2/auth/logout",
                              headers={'Content-Type': 'application/json',
                                       'Authorization': 'Bearer '+access_token})
        self.assertEqual(json.loads(res.data)["status"], 200)

    @pytest.mark.timeout(30)
    def test_successful_signout(self):
        """This method tests successful logout"""
        access_token = self.authenticateAdmin()
        self.client.put("/api/v2/auth/logout",
                        headers={'Content-Type': 'application/json',
                                 'Authorization': 'Bearer '+access_token})
        res = self.client.post("/api/v2/auth/signup",
                               data=json.dumps(signup_details),
                               headers={'Content-Type': 'application/json',
                                        'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(res.data)["Status"], 401)

    @pytest.mark.timeout(30)
    def test_protected_without_token(self):
        """This method tests access to protected route without a token"""
        res = self.client.post("/api/v2/auth/signup",
                               data=json.dumps(signup_details),
                               headers={'Content-Type': 'application/json'})
        self.assertEqual(res.status_code, 401)
        self.assertEqual(json.loads(res.data)["msg"], "Missing Authorization Header")
