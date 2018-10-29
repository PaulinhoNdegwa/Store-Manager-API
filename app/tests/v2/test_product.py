# from app.tests.v2.basetest import BaseTest
from app.tests.v2.basetest import BaseTest
from flask import json


class ProductTestCase(BaseTest):
    """Test suite for products"""

    def test_post_product(self):
        access_token = self.authenticate()
        response = self.client.post("/api/v2/products", data=self.product, 
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 201)

    def test_get_products(self):
        """"Test GET all products"""
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/products",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)

    def test_empty_product(self):
        access_token = self.authenticate()
        empty_product_details = {
            "product_name":" ",
            "model":" ",
            "product_price":1200,
            "quantity": 13,
            "min_quantity": 10
        }
        response = self.client.post("/api/v2/products", data=empty_product_details, 
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 201)

    def test_get_one_product(self):
        """"Test GET single product"""
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/products/1",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)

    def test_product_already_exists(self):
        """Test that API should not save the same product twice"""
        access_token = self.authenticate()
        response_1 = self.client.post("/api/v2/products", data=self.product, 
                header=dict(Authorization= "Bearer "+access_token))
        response_2 = self.client.post("/api/v2/products", data=self.product, 
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response_2.status_code, 409)

    def test_get_inexistent_product_id(self):
        """"Test GET inexistent product """
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/products/9",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 404)

    def test_update_product(self):
        """"Test update product"""
        access_token = self.authenticate()
        response = self.client.put( "/api/v2/products/1", data=json.dumps(self.product_update),
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)
    
    def test_delete_product(self):
        """"Test update product"""
        access_token = self.authenticate()
        response = self.client.delete( "/api/v2/products/1",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)