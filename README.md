# Store-Manager-API
This project involves building API endpoints for a Store Manager app. The following endpoints are the minimun required

EndPoint	Functionality	Notes

GET /products	Fetch all products	Get all available products.

GET /products/<productId>	Fetch a single product record	Get a specific product using the product’s id.
  
GET /sales	Fetch all sale records	Get all sale records. This endpoint should be accessible to only the store owner/admin.

GET /sales/<saleId>	Fetch a single sale record	Get a specific sale record using the sale record Id. This endpoint should be accessible to only the store owner/admin and the creator (store attendant) of the specific sale record.
  
POST /products	Create a product	Create a new product record. This endpoint should be accessible to only the store owner/admin.

POST /sales	Create a sale order	Create a sale record. This endpoint is accessible to only the store attendant.
