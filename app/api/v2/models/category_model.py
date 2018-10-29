from flask import jsonify, request, json
from db.db_config import open_connection, close_connection
from psycopg2 import Error
import psycopg2

class Category():
    """Creates category objects and methods"""

    def __init__(self):
        pass

    def save_category(self, cat_name, description):
        """Method to save a product"""

        if not cat_name or cat_name=="" or not description or description=="":
            return jsonify({
                "message":"Enter a category and description",
                "status":400
            })
        
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO categories(cat_name, cat_desc) VALUES (%s, %s) RETURNING id, cat_name, cat_desc",(cat_name, description,))
            new_category = cur.fetchone()
            print(new_category)
            category = {
                "category_id": new_category[0],
                "category_name": new_category[1],
                "description": new_category[2]
            }
            close_connection(conn)
            return jsonify({
                "message":"Category added successfully",
                "category_added": category,
                "status":200
            })
        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not add category", error)
            return jsonify({
                "message":"Category could not added",
                "status":400
            })


    def get_cat_by_id(self, cat_id):
        """Returns a category if it exists in the database"""

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM categories WHERE id = %s",(cat_id,))
            category_exists = cur.fetchone()
            close_connection(conn)

            return category_exists
        except (Exception, psycopg2.DatabaseError) as error:
            print("Could not retrieve category", error)

    def update_category(self, cat_id, cat_name, cat_desc):
        """Deletes a category record"""

        category_exists = self.get_cat_by_id(cat_id)

        if not category_exists:
            return jsonify({
                "message":"Category does not exist",
                "status":404
            })

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("UPDATE categories SET cat_name = %s, cat_desc = %s WHERE id = %s RETURNING id, cat_name, cat_desc", (cat_name, cat_desc, cat_id,))
            new_category = cur.fetchone()
            print(new_category)
            category = {
                "category_id": new_category[0],
                "category_name": new_category[1],
                "description": new_category[2]
            }
            close_connection(conn)
            return jsonify({
                "message":"Category added updated",
                "updated category": category,
                "status":200
            })
        except (Exception, psycopg2.DatabaseError) as error:
            print("Product could not be updated", error)
            return jsonify({
                "message":"Category could not updated",
                "status":400
            })

    def delete_category(self, cat_id):
        """Method to delete a category"""

        category_exists = self.get_cat_by_id(cat_id)

        if not category_exists:
            return jsonify({
                "message":"Category does not exist",
                "status":404
            })

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("DELETE FROM categories WHERE id = %s",(cat_id,))
            close_connection(conn)
            return jsonify({
                "message":"Category deleted",
                "status":200
            })
        except (Exception, psycopg2.DatabaseError) as error:
            print("Product could not be deleted", error)
            return jsonify({
                "message":"Category could not deleted",
                "status":400
            })
    