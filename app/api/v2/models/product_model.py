from flask import jsonify, request
from flask_jwt_extended import create_access_token
from db.db_config import open_connection, close_connection

products = []

class Product():
    """This class initialized a sales object. 
    Also it has a save method that saves the sale in a list"""

    def __init__(self):
        """Method to initialize Product list"""
        # self.products = products
        pass

    def get_product_by_id(self, product_id):
        """Fetches a product by product ID"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s ",(product_id,))
        product_exist = cur.fetchone()
        
        return product_exist


    def save_product(self, product_name, model, product_price, quantity, min_quantity, created_by):
        """Method to create and save a product dict object"""

        if not product_name or product_name=="" or not product_price :
            return jsonify({"message":"You must provide product details",
                            "status":400})
        
        if not request.json:
            return jsonify({"message":"Input should be in json format",
                            "status":400})
       
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_name = %s  and product_model = %s", (product_name,model,))
        product_exists = cur.fetchone()
        # print(product_exists)
        if product_exists:
            return jsonify({"message":"Product already exists",
                            "status":409})

        cur.execute("""INSERT INTO products(product_name, product_model, unit_price, quantity, min_quantity, created_by)
                 VALUES(%s, %s, %s, %s, %s, %s) RETURNING product_id, product_name, product_model, unit_price, quantity, min_quantity, created_by"""
                ,(product_name, model, product_price, quantity, min_quantity, created_by,))
        new_product = cur.fetchone()
        product = {
            "Product Id":new_product[0],
            "Product  Name":new_product[1],
            "Product Model":new_product[2],
            "Unit Price":new_product[3],
            "Quantity":new_product[4],
            "Min Quantity":new_product[5],
            "Created By": new_product[6]
        }
        close_connection(conn)
        return jsonify({"Message":"Successfully saved",
                        "Product id saved": product,
                        "status": 201})

    def update_product(self, product_id, product_name, model, product_price, quantity, min_quantity, created_by):
        if not product_name or product_name=="" or not product_price :
            return jsonify({"message":"You must provide product details",
                            "status":400})
        
        if not request.json:
            return jsonify({"message":"Input should be in json format",
                            "status":400})
        product_exist = self.get_product_by_id(product_id)
        
        print(product_exist)
        if not product_exist:
            return jsonify({"message":"Product does not exist",
                            "status":404})
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("""UPDATE products set product_name=%s, product_model=%s, unit_price=%s, quantity=%s, 
                    min_quantity=%s, created_by=%s WHERE product_id=%s RETURNING product_id, product_name,
                     product_model, unit_price, quantity, min_quantity, created_by""",
                    (product_name, model, product_price, quantity, min_quantity, created_by, product_id, ))
        updated_product = cur.fetchone()
        product = {
            "Product Id":updated_product[0],
            "Product  Name":updated_product[1],
            "Product Model":updated_product[2],
            "Unit Price":updated_product[3],
            "Quantity":updated_product[4],
            "Min Quantity":updated_product[5],
            "Updated by": updated_product[6]
        }
        close_connection(conn)
        return jsonify({"message":"Product successfully updated",
                        "Updated Product": product,
                        "status":200})
        
    def get_all_products(self):
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE quantity > 0")
        products = cur.fetchall()
        close_connection(conn)
        
        return products

    def get_single_product(self, product_id):
        """"Method to fetch single product"""

        if not product_id or not isinstance(product_id, int):
            return jsonify({"message":"Please provide a valid product id(int)",
                            "status":404})
        product_exist = self.get_product_by_id(product_id)
        if not product_exist:
            return jsonify({"message":"Product does not exist",
                            "status":404})
        product = {
            "product_id":product_exist[0],
            "product_name":product_exist[1],
            "product_model":product_exist[2],
            "unit":product_exist[3],
            "quantity":product_exist[4],
            "min quantity":product_exist[5]
        }
        return jsonify({"message":"Successful",
                        "product":product,
                        "status":200})


    def delete_product(self, product_id):
        """Method to delete product"""
        
        if not product_id or not isinstance(product_id, int):
            return jsonify({"message":"Please provide a valid product id(int)",
                            "status":404})
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_id = %s ",(product_id,))
        product_exist = cur.fetchall()
        
        print(product_exist)
        if not product_exist:
            return jsonify({"message":"Product does not exist",
                            "status":404})
        cur.execute("DELETE FROM products WHERE product_id=%s",(product_id,))
        close_connection(conn)
        return jsonify({"message":"Product sucessfully deleted",
                            "status":200})