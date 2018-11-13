from app.tests.v2.basetest import BaseTest
from flask import json
import pytest_timeout
import pytest
from .data import product, product_update, empty_product_details, category


class ProductTestCase(BaseTest):
    """Test suite for products"""

    def add_test_product(self):
        """Add a test product"""

        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/category", data=json.dumps(category),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.post("/api/v2/products", data=json.dumps(product),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        return response

    @pytest.mark.timeout(30)
    def test_post_product(self):
        """Test for new product"""

        response = self.add_test_product()
        self.assertEqual(json.loads(response.data)["status"], 201)
        self.assertEqual(json.loads(response.data)["message"],
                         "Successfully saved")

    @pytest.mark.timeout(30)
    def test_get_products(self):
        """"Test GET all products"""
        access_token = self.authenticate()
        self.add_test_product()
        response = self.client.get("/api/v2/products",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertIsInstance(json.loads(response.data)["Products"], list)

    @pytest.mark.timeout(30)
    def test_empty_product(self):
        """Test saving empty product details"""
        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/products", data=json.dumps(empty_product_details),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 400)
        self.assertEqual(json.loads(response.data)["message"],
                         "All fields are required")

    @pytest.mark.timeout(30)
    def test_get_one_product(self):
        """"Test GET single product"""
        self.add_test_product()
        access_token_2 = self.authenticate()
        response = self.client.get("/api/v2/products/1",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token_2})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Successful")

    @pytest.mark.timeout(30)
    def test_product_already_exists(self):
        """Test that API should not save the same product twice"""
        self.add_test_product()
        response = self.add_test_product()
        self.assertEqual(json.loads(response.data)["status"], 409)
        self.assertEqual(json.loads(response.data)["message"],
                         "Product already exists")

    @pytest.mark.timeout(30)
    def test_get_inexistent_product_id(self):
        """"Test GET inexistent product """
        access_token = self.authenticate()
        response = self.client.get("/api/v2/products/9",
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Product does not exist")

    @pytest.mark.timeout(30)
    def test_update_product(self):
        """"Test update product"""
        access_token = self.authenticateAdmin()
        self.add_test_product()
        response = self.client.put("/api/v2/products/1", data=json.dumps(product_update),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Product successfully updated")

    @pytest.mark.timeout(30)
    def test_delete_product(self):
        """"Test update product"""
        access_token = self.authenticateAdmin()
        self.add_test_product()
        response = self.client.delete("/api/v2/products/1",
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Product successfully deleted")
