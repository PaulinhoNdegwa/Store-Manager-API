from app.tests.v2.basetest import BaseTest
from flask import json
import pytest_timeout
import pytest
from .data import product, product_update, empty_product_details


class ProductTestCase(BaseTest):
    """Test suite for products"""

    @pytest.mark.timeout(30)
    def test_post_product(self):
        """Test for new product"""

        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/products", data=json.dumps(product),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 201)

    @pytest.mark.timeout(30)
    def test_get_products(self):
        """"Test GET all products"""
        access_token = self.authenticate()
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.get("/api/v2/products",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)

    @pytest.mark.timeout(30)
    def test_empty_product(self):
        """Test saving empty product details"""
        access_token = self.authenticateAdmin()

        response = self.client.post("/api/v2/products", data=json.dumps(empty_product_details),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 400)

    @pytest.mark.timeout(30)
    def test_get_one_product(self):
        """"Test GET single product"""
        access_token = self.authenticateAdmin()
        access_token_2 = self.authenticate()
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.get("/api/v2/products/1",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token_2})
        self.assertEqual(json.loads(response.data)["status"], 200)

    @pytest.mark.timeout(30)
    def test_product_already_exists(self):
        """Test that API should not save the same product twice"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/products", data=json.dumps(product),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 409)

    @pytest.mark.timeout(30)
    def test_get_inexistent_product_id(self):
        """"Test GET inexistent product """
        access_token = self.authenticate()
        response = self.client.get("/api/v2/products/9",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)

    @pytest.mark.timeout(30)
    def test_update_product(self):
        """"Test update product"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.put("/api/v2/products/1", data=json.dumps(product_update),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)

    @pytest.mark.timeout(30)
    def test_delete_product(self):
        """"Test update product"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/products", data=json.dumps(product),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.delete("/api/v2/products/1",
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
