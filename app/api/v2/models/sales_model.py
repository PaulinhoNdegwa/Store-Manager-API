from flask import jsonify, request, json
from db.db_config import open_connection, close_connection
from psycopg2 import Error
import psycopg2


class Sale():
    """This class initialized a sales object.
    Also it has a save method that saves the sale in a list"""

    def get_pdt_by_name_and_model(self, product_name, product_model):
        """Get product by name and model"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_name = %s\
         AND product_model = %s",
                    (product_name, product_model,))
        product_exists = cur.fetchone()
        close_connection(conn)
        return product_exists

    def create_sale(self, product_id, quantity, total_price, created_by):
        """Method to create sale record to DB"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO sales(product_id, quantity, total_price,\
             created_by) VALUES (%s, %s, %s, %s) \
             RETURNING product_id, quantity, \
             total_price, created_by, sale_id",
                        (product_id, quantity, total_price, created_by,))
            new_sale = cur.fetchone()
            sale = {
                "Product Id": new_sale[0],
                "Quantity": new_sale[1],
                "Total Price": new_sale[2],
                "Created_by": new_sale[3],
                "Sale Id": new_sale[4]
            }
            close_connection(conn)
            return sale

        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not save order", error)
            return jsonify({"message": "NOTSAVED",
                            "status": 400})

    def lookup_cart(self, product_id, current_user):
        """This method looks up if the current user has already added a
        similar product to cart"""

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT cart_id, quantity FROM carts WHERE product_id = %s\
        AND created_by=%s", (product_id, current_user,))
        cart_item_exists = cur.fetchone()
        close_connection(conn)
        return cart_item_exists

    def lookup_cart_by_username(self, current_user):
        """This method looks up if the current user has cart items"""

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM carts WHERE created_by=%s", (current_user,))
        cart_exists = cur.fetchall()
        close_connection(conn)
        return cart_exists

    def clear_cart(self, current_user):
        """This method deletes checked out cart items"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM carts WHERE created_by = %s",
                        (current_user,))
            close_connection(conn)
        except Exception as e:
            print(e)

    def add_to_cart(self, product_name, product_model, quantity, created_by):
        """Add items to cart"""

        product_exists = self.get_pdt_by_name_and_model(
            product_name, product_model)

        if not product_exists:
            return jsonify({"message": "Product not available",
                            "status": 404})
        product_id = product_exists[0]
        cart_item_exists = self.lookup_cart(product_id, created_by)
        if cart_item_exists:
            quantity = cart_item_exists[1]+quantity
            if quantity > (product_exists[5]-product_exists[6]):
                return jsonify({"message": "Unsufficient products. Check cart",
                                "status": 403})

            try:
                conn = open_connection()
                cur = conn.cursor()
                cur.execute("UPDATE carts SET quantity = %s, new_quantity=%s\
                            WHERE cart_id=%s",
                            (quantity, product_exists[5]-quantity,
                             cart_item_exists[0]))
                close_connection(conn)
            except Exception as e:
                print(e)
        else:
            if quantity > (product_exists[5]-product_exists[6]):
                return jsonify({"message": "Forbidden: Unsufficient products",
                                "status": 403})
            new_quantity = product_exists[5] - quantity
            total_price = product_exists[4]*quantity
            try:
                conn = open_connection()
                cur = conn.cursor()
                cur.execute("INSERT INTO carts(product_id, quantity, new_quantity,\
                total_price, created_by) VALUES (%s, %s, %s, %s, %s) \
                RETURNING product_id, quantity, \
                total_price, created_by, cart_id",
                            (product_id, quantity, new_quantity,
                             total_price, created_by,))
                close_connection(conn)

            except (Exception, psycopg2.DatabaseError) as e:
                print(e)

        cart_list = self.get_all_cart_items(created_by)

        return jsonify({
            "message": "Added {} item(s) of product id {} to cart".format(quantity, product_id),
            "Cart": cart_list,
            "status": 201
        })

    def get_all_cart_items(self, current_user):
        """This method retrieves all cart items added by a certain user"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("SELECT carts.cart_id, products.product_id, products.product_name,\
             products.product_model, carts.quantity, carts.total_price,\
              carts.created_by FROM \
             products INNER JOIN carts ON products.product_id = \
             carts.product_id WHERE carts.created_by = %s",
                        (current_user,))
            cart = cur.fetchall()
            close_connection(conn)
            cart_list = []
            for cart_item in cart:
                single_cart_item = {
                    "Cart_Id": cart_item[0],
                    "Product_Id": cart_item[1],
                    "Product_Name": cart_item[2],
                    "Product_Model": cart_item[3],
                    "Quantity": cart_item[4],
                    "Total_Price": cart_item[5],
                    "Created by": cart_item[6]
                }
                cart_list.append(single_cart_item)
            return cart_list
        except Exception as e:
            print(e)

    def subtract_products(self, new_quantity, product_id):

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("UPDATE products SET quantity = %s WHERE product_id = %s",
                    (new_quantity, product_id,))
        close_connection(conn)

    def checkout_cart(self, current_user):
        """This method saves the specific cart items in a users cart"""

        cart_exists = self.lookup_cart_by_username(current_user)
        if not cart_exists:
            return jsonify({
                "message": "No items in cart",
                "status": 404
            })
        sale_saved = []
        for cart_item in cart_exists:
            new_quantity = cart_item[4]
            product_id = cart_item[1]
            quantity = cart_item[3]
            total_price = cart_item[2]
            self.subtract_products(new_quantity, product_id)
            sale = self.create_sale(product_id, quantity, total_price,
                                    current_user)
            sale_saved.append(sale)

        self.clear_cart(current_user)
        return jsonify({"message": "Successfully saved",
                        "Sale_saved": sale_saved,
                        "status": 201})

    def remove_from_cart(self, cart_id):
        """Method to remove cart item"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM carts WHERE cart_id = %s ", (cart_id,))
            close_connection(conn)

            return jsonify({"message": "Cart item successfully removed",
                            "status": 200})

        except Exception as e:
            return jsonify({"message": "Could not remove cart item",
                            "Error": e})

    def get_single_sale(self, sale_id):
        """Method to get single sale"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE sale_id = %s ", (sale_id,))
        sale_exists = cur.fetchone()
        close_connection(conn)

        if not sale_exists:
            return jsonify({"message": "Sale not found",
                            "status": 404})
        sale = {
            "sale_id": sale_exists[0],
            "product_id": sale_exists[1],
            "total_price": sale_exists[2],
            "quantity": sale_exists[3],
            "attendant": sale_exists[4]
        }
        return jsonify({"Sale": sale,
                        "status": 200})

    def get_all_sales(self):
        """Method to return all products"""

        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales ")
        sales = cur.fetchall()
        close_connection(conn)

        if not sales:
            return jsonify({"message": "Sales not found",
                            "status": 404})
        sales_list = []
        for sale in sales:
            sale_dict = {
                "sale_id": sale[0],
                "product_id": sale[1],
                "total_price": sale[2],
                "quantity": sale[3],
                "attendant": sale[4]
            }
            sales_list.append(sale_dict)
        return jsonify({"message": "Successful",
                        "Sales": sales_list,
                        "status": 200})
