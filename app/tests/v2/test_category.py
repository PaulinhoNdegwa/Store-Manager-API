from app.tests.v2.basetest import BaseTest
from flask import json
import pytest
import pytest_timeout
from .data import *

class CategoryTestCase(BaseTest):
    """This is a test suite for categories"""

    def test_create_category(self):
        """This method test successful creation of a category"""

        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/category", data=json.dumps(new_category),
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 200)

    def test_create_with_no_cat_name(self):
        """This method tests for creation of a category with empty category name"""

        access_token = self.authenticateAdmin()
        response = self.client.post("/api/v2/category", data=json.dumps(invalid_category),
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 400)

    def test_create_cat_as_attendant(self):
        """This method tests creating a category as an attendant"""

        access_token = self.authenticate()
        response = self.client.post("/api/v2/category", data=json.dumps(new_category),
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 401)
    
    def test_update_category(self):
        """This method tests for the successful update of a category"""
        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/category", data=json.dumps(new_category),
                headers=dict(Authorization= "Bearer "+access_token))        
        response = self.client.put("/api/v2/category/1", data=json.dumps(update_category),
                headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 200)

    def test_delete_category_as_attendant(self):
        """This method tests the deletion of a category by an attendant"""

        access_token = self.authenticate()
        response = self.client.delete("/api/v2/category/1", 
                    headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 401)

    def test_delete_unavailable_category(self):
        """This method tests the deletion of a category that is not available"""

        access_token = self.authenticateAdmin()
        response = self.client.delete("/api/v2/category/1", 
                    headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 404)

    def test_successfully_delete_category(self):
        """This method tests the successfull deletion of a category"""

        access_token = self.authenticateAdmin()
        self.client.post("/api/v2/category", data=json.dumps(new_category),
                headers=dict(Authorization= "Bearer "+access_token))
        response = self.client.delete("/api/v2/category/1", 
                    headers=dict(Authorization= "Bearer "+access_token))
        self.assertEqual(json.loads(response.data)["status"], 200)