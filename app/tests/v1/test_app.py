import unittest
import pytest
from flask import json
from app import create_app

@pytest.fixture
def client():
    """This function creates a test client"""
    config = "testing"
    storemanager = create_app(config)
    test_client = storemanager.test_client()
    return test_client

def test_post_product(client):
    """
        Tests that a product can be successfully saved
    """
    product = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 38,
        "min_quantity": 10
    }
    response = client.post("/api/v1/products", data=json.dumps(product))
    assert json.loads(response.data)["status"] == 201

def test_get_all_products(client):
    """Test the get all products endpoint"""
    response = client.get("api/v1/products")
    data = json.loads(response.data)["Products"]
    assert isinstance(data, list)

def test_get_all_productsstatus(client):
    """Test the get all products endpoint"""
    response = client.get("api/v1/products")
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_product(client):
    """Test if the API can retrieve a single product"""
    response = client.get("api/v1/products/1")
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_product_length(client):
    """Test if the API can retrieve a single product"""
    response = client.get("api/v1/products/1")
    data = json.loads(response.data)["Product"]
    assert len(data) == 1


def test_get_unspecified_productid(client):
    """Tests if the api can retrieve a product that is not specified"""
    response = client.get("/api/v1/products/")
    assert response.status_code == 404

def test_get_nonint_productid(client):
    """Tests if the api can retrieve a product that is not specified"""
    response = client.get("/api/v1/products/j")
    assert response.status_code == 404


def test_empty_product_name(client):
    product = {
        "product_name":" ",
        "product_price": 900,
        "quantity": 38,
        "min_quantity": 10
    }
    response = client.post("/api/v1/products", data=json.dumps(product))
    assert response.status_code == 400


def test_get_unsaved_product(client):
    """This function tests if the API can retrieve a product whose id
    has not been saved"""
    response = client.get("/api/v1/products/20")
    assert json.loads(response.data)["status"] == 404



# TESTS FOR SALES
def test_post_sales(client):
    """
        Tests that a sale order can be successfully saved
    """
    sale = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 3,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale))
    assert json.loads(response.data)["status"] == 201

def test_get_all_sales(client):
    """Test the get all sales endpoint"""
    response = client.get("api/v1/sales")
    data = json.loads(response.data)["Sales"]
    assert isinstance(data, list)

def test_get_all_sales_status(client):
    """Test the get all sales endpoint success status code"""
    response = client.get("api/v1/sales")
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_sale_order(client):
    """Test if the API can retrieve a single sale order"""
    response = client.get("api/v1/sales/1")
    data = json.loads(response.data)["status"]
    assert data == 200

def test_save_unavailable(client):
    """Tests if the api creates a sale order of an unavalilable product"""
    sale = {
        "product_name":"HP",
        "product_price": 900,
        "quantity": 3,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale))
    assert json.loads(response.data)["status"] == 404

def test_order_excess(client):
    """Tests if the api creates a sale order of more items than the available products"""
    sale = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 200,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale))
    assert json.loads(response.data)["status"] == 403

def test_get_unspecified_saleid(client):
    """Tests if the api can retrieve a sale order that is not specified"""
    response = client.get("/api/v1/sales/")
    assert response.status_code == 404

def test_get_nonint_sale_productid(client):
    """Tests if the api can retrieve a sale order that is not specified"""
    response = client.get("/api/v1/sales/j")
    assert response.status_code == 404


def test_empty_sale_product_name(client):
    sale = {
        "product_name":" ",
        "product_price": 900,
        "quantity": 4,
        "attendant": "John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale))
    assert response.status_code == 400


def test_get_unsaved_sale_order(client):
    """This function tests if the API can retrieve a sale order whose id
    has not been saved"""
    response = client.get("/api/v1/sales/20")
    assert json.loads(response.data)["status"] == 404
