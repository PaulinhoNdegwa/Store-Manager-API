from app.tests.v2.basetest import BaseTest
from flask import json
import pytest_timeout
import pytest

class AuthTestCase(BaseTest):
    """Authentication test suite"""

    @pytest.mark.timeout(30)
    def test_successful_signup(self):
        """Function to test successful signup"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(self.admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(self.signup_details), 
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 201)

    @pytest.mark.timeout(30)
    def test_signup_with_invalid_email(self):
        """Function to test  signup with invalid email"""
        user = {
                "email": "paulgmail.com",
                "password": "1234",
                "confirm_password":"1234",
                "role":"Admin"
                
                }
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(self.admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(user), 
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 400)
    
    @pytest.mark.timeout(30)
    def test_login_with_invalid_password(self):
        """Function to test login with invalid password"""
        user = {
                "email": "paul@email.com",
                "password": "123456"
                }
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(self.admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        self.client.post("/api/v2/auth/signup", data=json.dumps(self.signup_details))              
        response = self.client.post("/api/v2/auth/login", data=json.dumps(user))
        self.assertEqual(json.loads(response.data)["status"], 400)

    @pytest.mark.timeout(30)
    def test_successful_login(self):
        """Function to test successful login"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/signup", data=json.dumps(self.signup_details), 
                headers=dict(Authorization= "Bearer "+access_token))      
        response = self.client.post("/api/v2/auth/login", data=json.dumps(self.login_details))
        self.assertEqual(json.loads(response.data)["status"], 200)
