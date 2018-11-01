from app.tests.v2.basetest import BaseTest
from flask import json
import pytest
import pytest_timeout
from .data import new_category, update_category, invalid_category


class CategoryTestCase(BaseTest):
    """This is a test suite for categories"""

    def test_create_category(self):
        """This method test successful creation of a category"""

        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/category", data=json.dumps(new_category),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Category added successfully")

    def test_create_with_no_cat_name(self):
        """This method tests for creation of a category with empty category name"""

        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/category", data=json.dumps(invalid_category),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 400)
        self.assertEqual(json.loads(response.data)["message"],
                         "Category name and description are required")

    def test_create_cat_as_attendant(self):
        """This method tests creating a category as an attendant"""

        access_token = self.authenticate()
        response = self.client.post("/api/v2/category", data=json.dumps(new_category),
                                    headers={'Content-Type': 'application/json',
                                             'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 401)
        self.assertEqual(json.loads(response.data)["message"],
                         "Unauthorized! You are not an admin")

    def test_update_category(self):
        """This method tests for the successful update of a category"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/category", data=json.dumps(new_category),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.put("/api/v2/category/1", data=json.dumps(update_category),
                                   headers={'Content-Type': 'application/json',
                                            'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Category updated")

    def test_delete_category_as_attendant(self):
        """This method tests the deletion of a category by an attendant"""

        access_token = self.authenticate()
        response = self.client.delete("/api/v2/category/1",
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 401)
        self.assertEqual(json.loads(response.data)["message"],
                         "Unauthorized! You are not an admin")

    def test_delete_unavailable_category(self):
        """This method tests the deletion of a category that is not available"""

        access_token = self.authenticateAdmin()
        response = self.client.delete("/api/v2/category/1",
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 404)
        self.assertEqual(json.loads(response.data)["message"],
                         "Category does not exist")

    def test_successfully_delete_category(self):
        """This method tests the successfull deletion of a category"""

        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/category", data=json.dumps(new_category),
                         headers={'Content-Type': 'application/json',
                                  'Authorization': 'Bearer ' + access_token})
        response = self.client.delete("/api/v2/category/1",
                                      headers={'Content-Type': 'application/json',
                                               'Authorization': 'Bearer ' + access_token})
        self.assertEqual(json.loads(response.data)["status"], 200)
        self.assertEqual(json.loads(response.data)["message"],
                         "Category deleted")
