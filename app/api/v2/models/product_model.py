from flask import jsonify, request
from flask_jwt_extended import create_access_token
from db.db_config import open_connection, close_connection
from app.api.v2.models.category_model import Category


class Product():
    """This class initialized a sales object.
    Also it has a save method that saves the sale in a list"""

    def get_product_by_id(self, product_id):
        """Fetches a product by product ID"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE product_id = %s ", (product_id,))
        product_exist = cur.fetchone()

        return product_exist

    def save_product(self, product_name, model, category, product_price,
                     quantity, min_quantity, created_by):
        """Method to create and save a product dict object"""
        category_available = Category().get_cat_by_name(category)

        if not category_available:
            category_id = None
        else:
            category_id = category_available[0]

        conn = open_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE product_name = %s  and product_model \
            = %s", (product_name, model,))
        product_exists = cur.fetchone()
        if product_exists:
            return jsonify({"message": "Product already exists",
                            "status": 409})

        cur.execute("""INSERT INTO products(product_name, product_model, \
                cat_id, unit_price, quantity, min_quantity, created_by)\
                 VALUES(%s, %s, %s, %s, %s, %s, %s) RETURNING product_id, \
                 product_name, product_model, unit_price, quantity,\
                  min_quantity, created_by""",
                    (product_name, model, category_id, product_price, quantity,
                     min_quantity, created_by,))
        new_product = cur.fetchone()
        product = {
            "Product Id": new_product[0],
            "Product Name": new_product[1],
            "Product Model": new_product[2],
            "Unit Price": new_product[3],
            "Quantity": new_product[4],
            "Min Quantity": new_product[5],
            "Created By": new_product[6]
        }
        close_connection(conn)
        return jsonify({"message": "Successfully saved",
                        "Product id saved": product,
                        "status": 201})

    def update_product(self, product_id, product_name, model, product_price,
                       quantity, min_quantity, created_by):
        """This method allows an admin to update the products details"""

        product_exist = self.get_product_by_id(product_id)
        print(product_exist)
        if not product_exist:
            return jsonify({"message": "Product does not exist",
                            "status": 404})
        quantity = int(quantity)
        min_quantity = int(min_quantity)
        new_quantity = product_exist[5] + quantity

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("""UPDATE products set product_name=%s, product_model=%s, \
                    unit_price=%s, quantity=%s, min_quantity=%s, created_by=%s\
                    WHERE product_id=%s RETURNING product_id, product_name,\
                    product_model, unit_price, quantity, min_quantity, \
                    created_by""",
                    (product_name, model, product_price, new_quantity,
                     min_quantity, created_by, product_id, ))
        updated_product = cur.fetchone()
        product = {
            "Product Id": updated_product[0],
            "Product  Name": updated_product[1],
            "Product Model": updated_product[2],
            "Unit Price": updated_product[3],
            "Quantity": updated_product[4],
            "Min Quantity": updated_product[5],
            "Updated by": updated_product[6]
        }
        close_connection(conn)
        return jsonify({"message": "Product successfully updated",
                        "Updated Product": product,
                        "status": 200})

    def get_all_products(self):
        """This method returns all products that are available"""

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE quantity > 0")
        products = cur.fetchall()
        close_connection(conn)
        product_list = []
        for product in products:
            product_dict = {
                "product_id": product[0],
                "product_name": product[1],
                "product_model": product[2],
                "category": product[3],
                "unit_price": product[4],
                "quantity": product[5],
                "min_quantity": product[6]
            }
            product_list.append(product_dict)

        return product_list

    def get_single_product(self, product_id):
        """"Method to fetch single product"""

        if not product_id or not isinstance(product_id, int):
            return jsonify({"message": "Please provide a valid product id",
                            "status": 404})
        product_exist = self.get_product_by_id(product_id)
        if not product_exist:
            return jsonify({"message": "Product does not exist",
                            "status": 404})
        product = {
            "product_id": product_exist[0],
            "product_name": product_exist[1],
            "product_model": product_exist[2],
            "Category": product_exist[3],
            "unit": product_exist[4],
            "quantity": product_exist[5],
            "min quantity": product_exist[6]
        }
        return jsonify({"message": "Successful",
                        "product": product,
                        "status": 200})

    def delete_product(self, product_id):
        """Method to delete product"""

        if not product_id or not isinstance(product_id, int):
            return jsonify({"message": "Please provide a valid product id",
                            "status": 404})
        conn = open_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM products WHERE product_id = %s ", (product_id,))
        product_exist = cur.fetchall()

        if not product_exist:
            return jsonify({"message": "Product does not exist",
                            "status": 404})
        cur.execute("DELETE FROM products WHERE product_id=%s", (product_id,))
        close_connection(conn)
        return jsonify({"message": "Product successfully deleted",
                        "status": 200})
