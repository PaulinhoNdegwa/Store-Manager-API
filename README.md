[![Build Status](https://travis-ci.com/PaulinhoNdegwa/Store-Manager-API.svg?branch=develop)](https://travis-ci.com/PaulinhoNdegwa/Store-Manager-API)
[![Coverage Status][![Coverage Status](https://coveralls.io/repos/github/PaulinhoNdegwa/Store-Manager-API/badge.svg?branch=develop)](https://coveralls.io/github/PaulinhoNdegwa/Store-Manager-API?branch=develop)
[![Maintainability](https://api.codeclimate.com/v1/badges/613b98b77564d6e19702/maintainability)](https://codeclimate.com/github/PaulinhoNdegwa/Store-Manager-API/maintainability)


# Store-Manager-API 

This project involves building API endpoints for a Store Manager app. The following endpoints are the minimun required

EndPoint	Functionality	Notes

GET /products	Fetch all products	Get all available products.

GET /products/<productId>	Fetch a single product record	Get a specific product using the product’s id.
  
GET /sales	Fetch all sale records	Get all sale records. This endpoint should be accessible to only the store owner/admin.

GET /sales/<saleId>	Fetch a single sale record	Get a specific sale record using the sale record Id. This endpoint should be accessible to only the store owner/admin and the creator (store attendant) of the specific sale record.
  
POST /products	Create a product	Create a new product record. This endpoint should be accessible to only the store owner/admin.

POST /sales	Create a sale order	Create a sale record. This endpoint is accessible to only the store attendant.
