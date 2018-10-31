from flask import jsonify, request, json
from db.db_config import open_connection, close_connection
from psycopg2 import Error
import psycopg2

class Sale():
    """This class initialized a sales object. 
    Also it has a save method that saves the sale in a list"""

    def __init__(self):
        """Method to initialize sales"""
        pass

    def get_pdt_by_name_and_model(self, product_name, product_model):
        """Get product by name and model"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE product_name = %s AND product_model = %s", (product_name, product_model,))
        product_exists = cur.fetchall()
        close_connection(conn)
        return product_exists

    def create_sale(self, product_id, quantity, total_price, created_by):
        """Method to create sale record to DB"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO sales(product_id, quantity, total_price, created_by) VALUES (%s, %s, %s, %s) RETURNING product_id, quantity, total_price, created_by",
                        (product_id, quantity, total_price, created_by,))
            new_sale = cur.fetchone()
            sale = {
                "Product Id":new_sale[0],
                "Quantity": new_sale[1],
                "Total Price": new_sale[2],
                "Created_by": new_sale[3]
            }
            close_connection(conn)
            return jsonify({"message":"Successfully saved",
                        "Product id recorded": sale,
                        "status": 201})

        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not save order", error)
            return jsonify({"message":"NOTSAVED",
                        "status": 400})

    def subtract_products(self, new_quantity, product_id):
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("UPDATE products SET quantity = %s WHERE product_id = %s",(new_quantity, product_id,))
        close_connection(conn)

    def save_sale(self, product_name, product_model, quantity, current_user):
        
        if product_name=="" or not product_name:
            return jsonify({"message":"You must provide product details",
                            "status":400})
        
        if not request.json:
            return jsonify({"message":"Input should be in json format",
                            "status":400})

        product_exists = self.get_pdt_by_name_and_model(product_name, product_model)
        print(product_exists)        

        if not product_exists:
            return jsonify({"message":"Product not available",
                            "status":404})
        if quantity > (product_exists[0][5]-product_exists[0][6]):
            return jsonify({"message":"Forbidden: There are fewer products than requested",
                            "status":403})
        new_quantity = product_exists[0][5] - quantity
        total_price = product_exists[0][4]*quantity
        product_id = product_exists[0][0]
        self.subtract_products(new_quantity, product_id)
        
        return self.create_sale(product_id, quantity, total_price, current_user)


    def get_single_sale(self, sale_id):
        """Method to get single sale"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales WHERE sale_id = %s ", (sale_id,))
        sale_exists = cur.fetchone()
        close_connection(conn)

        if not sale_exists:
            return jsonify({"message":"Sale not found",
                            "status": 404})
        sale ={
            "sale_id": sale_exists[0],
            "product_id": sale_exists[1],
            "total_price":sale_exists[2],
            "quantity":sale_exists[3],
            "attendant":sale_exists[4]
        }
        return jsonify({"Sale" : sale,
                            "status" : 200})

    def get_all_sales(self):
        """Method to return all products"""
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM sales ")
        sales= cur.fetchall()
        close_connection(conn)

        if not sales:
            return jsonify({"message":"Sales not found",
                            "status": 404})
        sales_list= []
        for sale in sales:
            sale_dict ={
                "sale_id": sale[0],
                "product_id": sale[1],
                "total_price":sale[2],
                "quantity":sale[3],
                "attendant":sale[4]
            }
            sales_list.append(sale_dict)
        return jsonify({ "message": "Successful",
                        "Sales" : sales_list,
                        "status" : 200})