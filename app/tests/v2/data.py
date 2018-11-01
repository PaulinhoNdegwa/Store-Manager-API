
# ###################CATEGORY TEST DATA#######################
new_category = {
    "cat_name": "Phones",
    "desc": "Category for mobile phones"
}

invalid_category = {
    "cat_name": " ",
    "desc": "Category for mobile phones"
}

update_category = {
    "cat_name": "Mobile Phones",
    "desc": "Category for mobile phones"
}

# ###################AUTHENTICATION TEST DATA#######################
admin_login = {
    "email": "admin@gmail.com",
    "password": "Qwerty1"
}
signup_details = {
    "email": "paul@gmail.com",
    "password": "1234QWEr",
    "confirm_password": "1234QWEr",
    "role": "Attendant"
}

login_details = {
    "email": "paul@gmail.com",
    "password": "1234QWEr"
}
invalid_email = {
    "email": "paulgmail.com",
    "password": "1234",
    "confirm_password": "1234",
    "role": "Admin"

}

# ###################PRODUCT TEST DATA#######################
product = {
    "product_name": "macbook",
    "model": "g3",
    "category": "Laptop",
    "product_price": 1200,
    "quantity": 29,
    "min_quantity": 10
}

product_update = {
    "product_name": "macbook",
    "model": "g4",
    "category": "Laptop",
    "product_price": 1200,
    "quantity": 27,
    "min_quantity": 10
}
empty_product_details = {
    "product_name": " ",
    "model": " ",
    "category": "Laptop",
    "product_price": 1200,
    "quantity": 13,
    "min_quantity": 10
}
# ###################SALE TEST DATA#######################
sale = {
    "product_name": "macbook",
    "product_model": "g3",
    "quantity": 5
}

sale_update = {
    "product_name": "HP",
    "model": "15",
    "quantity": 7
}
empty_sale_details = {
    "product_name": " ",
    "product_model": " ",
    "quantity": 5
}
# ###################USERS TEST DATA#######################
new_role = {
    "role": "admin"
}

# headers
access_token = ""
header_with_token = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer ' + access_token
}

header_without_token = {
    'Content-Type': 'application/json'
}
