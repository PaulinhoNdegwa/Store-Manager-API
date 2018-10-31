import unittest
from flask import json
from db import tables
from app import create_app
from .data import signup_details, admin_login, login_details, header_without_token


config_name = "testing"
class BaseTest(unittest.TestCase):
    tables.drop_tables()
    def setUp(self):
        
        tables.create_tables()
        storemanager = create_app(config_name)
        storemanager.testing =True
        self.client = storemanager.test_client()
        
        
    def authenticateAdmin(self):
        print(admin_login)
        response = self.client.post("api/v2/auth/login", 
                    data=json.dumps(admin_login), 
                    headers=header_without_token)
        access_token = json.loads(response.data)["token"]
        # print("Admin token",access_token)
        return access_token

    def authenticate(self):
        access_token = self.authenticateAdmin()
        self.client.post("api/v2/auth/signup", data=json.dumps(signup_details),
                        headers={'Content-Type': 'application/json',
                                'Authorization': 'Bearer ' + access_token})
        response = self.client.post("api/v2/auth/login", data=json.dumps(login_details),
                        headers=header_without_token)
        access_token = json.loads(response.data)["token"]
        # print("Attendant",access_token)
        return access_token    
    
    def tearDown(self):
        tables.drop_tables()
        