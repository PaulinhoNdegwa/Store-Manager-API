import unittest
from flask import json
from db import tables
from app import create_app



config_name = "testing"
class BaseTest(unittest.TestCase):

    def setUp(self):
        tables.create_tables()
        storemanager = create_app(config_name)
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
            "model":"g3",
            "product_price": 200,
            "quantity": 7,
            "attendant": "paul@gmail.com"
        }

        self.sale_update = {
            "product_name": "HP",
            "model":"15",
            "product_price": 200,
            "quantity": 7,
            "attendant": "paul@gmail.com"
        }

        self.product_update = {
            "product_name": "macbook",
            "model": "g4",
            "product_price": 1200,
            "quantity": 27,
            "min_quantity": 10
        }

        self.signup_details = {
            "email":"paul@email.com",
            "password":"1234",
            "admin": False
        }

        self.login_details = {
            "email":"paul@email.com",
            "password":"1234"
        }

    def authenticate(self):
        self.client.post("api/v2/signup", data=json.dumps(self.signup_details))
        response = self.client.post("api/v2/login", data=json.dumps(self.login_details))
        access_token = json.dumps(response.data)["access_token"]
        return access_token
    
    def tearDown(self):
        tables.drop_tables()