import unittest
from flask import json
from db import tables
from app import create_app


config_name = "testing"
class BaseTest(unittest.TestCase):
    tables.drop_tables()
    def setUp(self):
        
        tables.create_tables()
        storemanager = create_app(config_name)
        storemanager.testing =True
        self.client = storemanager.test_client()
        self.product = {
            "product_name": "macbook",
            "model": "g3",
            "product_price": 1200,
            "quantity": 29,
            "min_quantity": 10
        }
        self.sale = {
            "product_name": "macbook",
            "product_model":"g3",
            "quantity": 5
        }

        self.sale_update = {
            "product_name": "HP",
            "model":"15",
            "quantity": 7
        }

        self.product_update = {
            "product_name": "macbook",
            "model": "g4",
            "product_price": 1200,
            "quantity": 27,
            "min_quantity": 10
        }
        self.admin_login = {
            "email":"admin@gmail.com",
            "password":"Qwerty1"
        }
        self.signup_details = {
            "email":"paul@gmail.com",
            "password":"1234QWEr",
            "confirm_password":"1234QWEr",
            "role": "Attendant"
        }

        self.login_details = {
            "email":"paul@gmail.com",
            "password":"1234QWEr"
        }

    def authenticateAdmin(self):
        response = self.client.post("api/v2/auth/login", 
                    data=json.dumps(self.admin_login))
        access_token = json.loads(response.data)["token"]
        # print("Admin token",access_token)
        return access_token

    def authenticate(self):
        access_token = self.authenticateAdmin()
        self.client.post("api/v2/auth/signup", data=json.dumps(self.signup_details),
                        headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.post("api/v2/auth/login", 
                        data=json.dumps(self.login_details))
        access_token = json.loads(response.data)["token"]
        # print("Attendant",access_token)
        return access_token    
    
    def tearDown(self):
        tables.drop_tables()
        