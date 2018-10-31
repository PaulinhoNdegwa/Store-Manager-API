register_schema = {
    "type": "object",
    "properties": {
        "email": {type: "string"},
        "password": {type: "string"},
        "confirm_password": {type: "string"},
        "role": {type: "string"}
    },
    "required": ["email", "password", "confirm_password", "role"]
}

login_schema = {
    "type": "object",
    "properties": {
        "email": {type: "string"},
        "password": {type: "string"}
    },
    "required": ["email", "password"]
}

product_schema = {
    "type": "object",
    "properties": {
        "product_name": {type: "string"},
        "model": {type: "string"},
        "product_price": {type: "integer"},
        "quantity": {type: "integer"},
        "min_quantity": {type: "integer"}
    },
    "required": ["product_name", "model", "product_price", "quantity",
                 "min_quantity"]
}

new_sale_schema = {
    "type": "object",
    "properties": {
        "product_name": {type: "string"},
        "product_model": {type: "string"},
        "quantity": {type: "integer"}
    },
    "required": ["product_name", "product_model", "quantity"]
}

category_schema = {
    "type": "object",
    "properties": {
        "cat_name": {type: "string"},
        "desc": {type: "string"}
    },
    "required": ["cat_name", "desc"]
}

update_role_schema = {
    "type": "object",
    "properties": {
        "role": {type: "string"}
    },
    "required": ["role"]
}
