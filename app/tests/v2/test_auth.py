from app.tests.v2.basetest import BaseTest
from flask import json
import pytest_timeout
import pytest
from .data import admin_login, signup_details, login_details, invalid_email

class AuthTestCase(BaseTest):
    """Authentication test suite"""

    @pytest.mark.timeout(30)
    def test_successful_signup(self):
        """Function to test successful signup"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(signup_details), 
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 201)

    @pytest.mark.timeout(30)
    def test_signup_with_invalid_email(self):
        """Function to test  signup with invalid email"""

        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("/api/v2/auth/signup", data=json.dumps(invalid_email), 
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
        self.client.post("/api/v2/auth/login", data=json.dumps(admin_login), 
                headers=dict(Authorization= "Bearer "+access_token))
        self.client.post("/api/v2/auth/signup", data=json.dumps(signup_details))              
        response = self.client.post("/api/v2/auth/login", data=json.dumps(user))
        self.assertEqual(json.loads(response.data)["status"], 400)

    @pytest.mark.timeout(30)
    def test_successful_login(self):
        """Function to test successful login"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/auth/signup", data=json.dumps(signup_details), 
                headers=dict(Authorization= "Bearer "+access_token))      
        response = self.client.post("/api/v2/auth/login", data=json.dumps(login_details))
        self.assertEqual(json.loads(response.data)["status"], 200)
