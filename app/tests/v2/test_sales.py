from app.tests.v2.basetest import BaseTest
from flask import json


class SalesTestCase(BaseTest):
    """Test suite for sales"""

    def test_post_sale(self):
        access_token = self.authenticate()
        response = self.client.post("/api/v2/sales", data=self.sale, 
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 201)

    def test_get_sales(self):
        """"Test GET all sales orders"""
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/sales",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)

    def test_empty_sale(self):
        access_token = self.authenticate()
        empty_sale_details = {
            "product_name":" ",
            "model":" ",
            "product_price":1200,
            "quantity": 5
        }
        response = self.client.post("/api/v2/sales", data=empty_sale_details, 
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 201)

    def test_get_one_sale(self):
        """"Test GET single sale order"""
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/sales/1",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)

    
    def test_get_inexistent_sale_id(self):
        """"Test GET inexistent sale order """
        access_token = self.authenticate()
        response = self.client.get( "/api/v2/sales/9",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 404)

    def test_update_sale(self):
        """"Test update product"""
        access_token = self.authenticate()
        response = self.client.put( "/api/v2/sales/1", data=json.dumps(self.sale_update),
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)

    def test_delete_sale(self):
        """"Test update product"""
        access_token = self.authenticate()
        response = self.client.delete( "/api/v2/sales/1",
                header=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(response.status_code, 200)