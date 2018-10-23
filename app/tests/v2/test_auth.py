from app.tests.v2.basetest import BaseTest
from flask import json


class AuthTestCase(BaseTest):
    """Authentication test suite"""

    def test_successful_signup(self):
        """Function to test successful signup"""    
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(self.signup_details))
        self.assertEqual(response.status_code, 201)

    def test_signup_with_invalid_email(self):
        """Function to test  signup with invalid email"""
        data = {
                "email": "paulgmail.com",
                "password": "1234",
                "role":"admin"
                
                }        
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(data))
        self.assertEqual(response.status_code, 400)

    def test_login_with_invalid_password(self):
        """Function to test login with invalid password"""
        data = {
                "email": "paul@gmail.com",
                "password": "123456"
                }        
        response = self.client.post("/api/v2/auth/login", data=json.dumps(data))
        self.assertEqual(response.status_code, 404)

    def test_successful_login(self):
        """Function to test successful signup"""        
        response = self.client.post("/api/v1/auth/login", data=json.dumps(self.login_details))
        self.assertEqual(response.status_code, 200)
