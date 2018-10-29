import unittest
from flask import json
from db import tables
from app import create_app
from .data import signup_details, admin_login, login_details


config_name = "testing"
class BaseTest(unittest.TestCase):
    tables.drop_tables()
    def setUp(self):
        
        tables.create_tables()
        storemanager = create_app(config_name)
        storemanager.testing =True
        self.client = storemanager.test_client()
        
        
    def authenticateAdmin(self):
        response = self.client.post("api/v2/auth/login", 
                    data=json.dumps(admin_login))
        access_token = json.loads(response.data)["token"]
        # print("Admin token",access_token)
        return access_token

    def authenticate(self):
        access_token = self.authenticateAdmin()
        self.client.post("api/v2/auth/signup", data=json.dumps(signup_details),
                        headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("api/v2/auth/login", 
                        data=json.dumps(login_details))
        access_token = json.loads(response.data)["token"]
        # print("Attendant",access_token)
        return access_token    
    
    def tearDown(self):
        tables.drop_tables()
        