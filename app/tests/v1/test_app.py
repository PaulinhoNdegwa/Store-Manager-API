import unittest
import pytest
from flask import json
from app import create_app

# Create test data for authentication
signup_data = {
            "email": "paul@gmail.com",
            "password": "1234",
            "role":"admin"
            
            }
login_data = {
        "email":"paul@gmail.com",
        "password":"1234"
    }

@pytest.fixture
def client():
    """This function creates a test client"""
    config = "testing"
    storemanager = create_app(config)
    test_client = storemanager.test_client()
    return test_client
    

def authenticate(client):
    """Function successful signs up and logs in the client in order to access other operations
    It returns a login authentication token"""
    
    client.post("/api/v1/auth/signup", data=json.dumps(signup_data))
       
    response = client.post("/api/v1/auth/login", data=json.dumps(login_data))
    access_token = json.loads(response.data)["token"]
    return access_token

def test_successful_signup(client):
    """Function to test successful signup"""
    
    response = client.post("/api/v1/auth/signup", data=json.dumps(signup_data))
    assert json.loads(response.data)["status"] == 201

def test_signup_with_invalid_email(client):
    """Function to test  signup with invalid email"""
    data = {
            "email": "paulgmail.com",
            "password": "1234",
            "role":"admin"
            
            }
    
    response = client.post("/api/v1/auth/signup", data=json.dumps(data))
    assert json.loads(response.data)["status"] == 400

def test_successful_login(client):
    """Function to test successful signup"""
    
    response = client.post("/api/v1/auth/login", data=json.dumps(login_data))
    assert json.loads(response.data)["status"] == 201

def test_post_product(client):
    """
        Tests that a product can be successfully saved
    """
    access_token = authenticate(client)
    product = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 38,
        "min_quantity": 10
    }
    response = client.post("/api/v1/products", data=json.dumps(product)
    , headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 201

def test_get_all_products(client):
    """Test the get all products endpoint"""
    access_token = authenticate(client)
    response = client.get("api/v1/products" , headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["Products"]
    assert isinstance(data, list)

def test_get_all_productsstatus(client):
    """Test the get all products endpoint"""
    access_token = authenticate(client)
    response = client.get("api/v1/products"  , headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_product(client):
    """Test if the API can retrieve a single product"""
    access_token = authenticate(client)
    response = client.get("api/v1/products/1", headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_product_length(client):
    """Test if the API can retrieve a single product"""
    access_token = authenticate(client)
    response = client.get("api/v1/products/1", headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["Product"]
    assert len(data) == 1


def test_get_unspecified_productid(client):
    """Tests if the api can retrieve a product that is not specified"""
    access_token = authenticate(client)
    response = client.get("/api/v1/products/ " , headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 404

def test_get_nonint_productid(client):
    """Tests if the api can retrieve a product that is not specified"""
    access_token = authenticate(client)
    response = client.get("/api/v1/products/j" , headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 404


def test_empty_product_name(client):
    
    access_token = authenticate(client)
    product = {
        "product_name":" ",
        "product_price": 900,
        "quantity": 38,
        "min_quantity": 10
    }
    response = client.post("/api/v1/products", data=json.dumps(product), headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 400


def test_get_unsaved_product(client):
    """This function tests if the API can retrieve a product whose id
    has not been saved"""
    access_token = authenticate(client)
    response = client.get("/api/v1/products/20", headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 404



# TESTS FOR SALES
def test_post_sales(client):
    """
        Tests that a sale order can be successfully saved
    """
    access_token = authenticate(client)
    sale = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 3,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale), headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 201

def test_get_all_sales(client):
    """Test the get all sales endpoint"""
    access_token = authenticate(client)
    response = client.get("api/v1/sales", headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["Sales"]
    assert isinstance(data, list)

def test_get_all_sales_status(client):
    """Test the get all sales endpoint success status code"""
    access_token = authenticate(client)
    response = client.get("api/v1/sales" , headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["status"]
    assert data == 200


def test_single_sale_order(client):
    """Test if the API can retrieve a single sale order"""
    access_token = authenticate(client)
    response = client.get("api/v1/sales/1", headers=dict(Authorization="Bearer "+access_token))
    data = json.loads(response.data)["status"]
    assert data == 200

def test_save_unavailable(client):
    """Tests if the api creates a sale order of an unavalilable product"""
    access_token = authenticate(client)
    sale = {
        "product_name":"HP",
        "product_price": 900,
        "quantity": 3,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale), headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 404

def test_order_excess(client):
    """Tests if the api creates a sale order of more items than the available products"""
    access_token = authenticate(client)
    sale = {
        "product_name":"Macbook",
        "product_price": 900,
        "quantity": 200,
        "attendant":"John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale), headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 403

def test_get_unspecified_saleid(client):
    """Tests if the api can retrieve a sale order that is not specified"""
    access_token = authenticate(client)
    response = client.get("/api/v1/sales/ ", headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 404

def test_get_nonint_sale_productid(client):
    """Tests if the api can retrieve a sale order that is not specified"""
    access_token = authenticate(client)
    response = client.get("/api/v1/sales/j", headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 404


def test_empty_sale_product_name(client):
    
    access_token = authenticate(client)
    sale = {
        "product_name":" ",
        "product_price": 900,
        "quantity": 4,
        "attendant": "John Doe"
    }
    response = client.post("/api/v1/sales", data=json.dumps(sale) , headers=dict(Authorization="Bearer "+access_token))
    assert response.status_code == 400


def test_get_unsaved_sale_order(client):
    """This function tests if the API can retrieve a sale order whose id
    has not been saved"""
    
    access_token = authenticate(client)
    response = client.get("/api/v1/sales/20" , headers=dict(Authorization="Bearer "+access_token))
    assert json.loads(response.data)["status"] == 404
