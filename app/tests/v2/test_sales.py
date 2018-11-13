from app.tests.v2.basetest import BaseTest
from flask import json
from .data import sale, sale_update, product, empty_sale_details, category


class SalesTestCase(BaseTest):
    """Test suite for sales"""

    def add_test_sale(self):
        """Add a test product"""

        access_token = self.authenticateAdmin()
        access_token_2 = self.authenticate()
        self.client.post("/api/v2/category", data=json.dumps(category),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/sales", data=json.dumps(sale),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token_2})
        print(json.loads(response.data))
        return response

    def test_post_sale(self):

        response = self.add_test_sale()

        self.assertEqual(json.loads(response.data)["status"], 201)

    def test_get_sales(self):
        """"Test GET all sales orders"""
        access_token = self.authenticate()
        access_token_2 = self.authenticateAdmin()
        self.add_test_sale()
        self.client.post("/api/v2/cart",
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.get("/api/v2/sales",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token_2})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Successful")

    def test_empty_sale(self):
        access_token = self.authenticate()

        response = self.client.post("/api/v2/sales", data=json.dumps(empty_sale_details),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Product_name, product_model, quantity required")

    def test_get_one_sale(self):
        """"Test GET single sale order"""
        access_token = self.authenticate()
        access_token_2 = self.authenticateAdmin()
        self.add_test_sale()
        self.client.post("/api/v2/cart",
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.get("/api/v2/sales/1",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token_2})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertIsInstance(json.loads(response.data)["Sale"], dict)

    def test_get_inexistent_sale_id(self):
        """"Test GET inexistent sale order """
        access_token = self.authenticateAdmin()
        response = self.client.get("/api/v2/sales/9",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Sale not found")
