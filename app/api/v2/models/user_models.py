from flask import jsonify, request
from flask_jwt_extended import create_access_token
import re
from psycopg2 import Error
import psycopg2
from db.db_config import open_connection, close_connection
from werkzeug.security import generate_password_hash, check_password_hash

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"

class User():
    """This class initialized a user object."""

    def __init__(self):
        pass

    def validate_password(self, password):
        """Method to validate a password. A password must be between 6-8 characters, 
        one lower case, one uppercase and a number"""
        while True:
            if not re.search("[A-Z]", password):
                break
            elif not re.search("[a-z]", password):
                break
            elif len(password) > 8 or len(password) < 6:
                break
            elif not re.search("[0-9]", password):
                break
            else:
                return True
        return jsonify({"message": "Please use a valid password format",
                            "details": "Password len(6-8), must have lower case, uppercase and number",
                            "status": 400})

    def validate_role(self, role):
        """This methods validate that role is either Admin or Attendant"""

        role = role.lower()
        if role == "admin" or role == "attendant":
            return True
        return False
    
    def validate_email(self, email):
        """This method validates email addresses"""
        if not re.match(email_format, email):
            return jsonify({"message": "Please use a valid email format",
                            "status": 400})
        return True

    def save_user(self, email, password, confirm_password, role):
        
        if not request.get_json:
            return jsonify({"message":"Data must be in json format",
                            "status": 400})

        if not email or not password or not confirm_password:
            return jsonify({"message":"You must provide email and password",
                            "status": 400})

        valid_email = self.validate_email(email)
        if valid_email != True:
            return valid_email
                
        is_password = self.validate_password(password)
        if is_password != True:
            return is_password
        if password != confirm_password:
            return jsonify({"message": "Passwords do not match.",
                            "status": 400})

        validate_role = self.validate_role(role)
        if not validate_role:
                  return jsonify({"message": "Role can only be admin or attendant",
                            "status": 400})

        password = generate_password_hash(password)
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = %s ",(email,))
            user_exists = cur.fetchone()

            if user_exists:
                return jsonify({"message":"User already exists",
                                "status": 400})
            else:
                cur.execute("INSERT INTO users(username, password, role) VALUES (%s,%s,%s) ", (email, password, role,))            
                close_connection(conn)
                return jsonify({
                    "message":"User saved",
                    "email":email,
                    "status": 201
                })   
            
        except (Exception ,psycopg2.DatabaseError) as error:
            print(error)
            return jsonify({"message":"Error when saving user!"})

    
    def user_login(self, email, password):
        """Method to log in a user"""

        if not request.get_json:
            return jsonify("Data must be in json format")
        if not email or not password:
            return jsonify("You must provide username and password")
            
        valid_email = self.validate_email(email)
        if valid_email != True:
            return valid_email

        is_password = self.validate_password(password)
        if is_password != True:
            return is_password
            
        conn = open_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (email, ))
        user_exists = cur.fetchone()
        # print(user_exists)
        close_connection(conn)
        if not user_exists:
            return jsonify({
                "message":"User does not exist",
                "status":400
            })
        
        role = user_exists[3]
        db_password =user_exists[2]
        password_correct = check_password_hash(db_password, password)
        if not password_correct:
            return jsonify({
                "message":"Incorrect password",
                "status": 400
            })

        user_identity = {
            "username":email,
            "role":role
        }
        access_token = create_access_token(identity=user_identity)
        # print(access_token)
        token_available = self.lookup_token(access_token)
        if token_available:
            return jsonify({
                "message":"Token generated already exists",
                "status":409
            })
        return jsonify({
            "message":"Successfully logged in",
            "token": access_token,
            "status": 200
        })

       

    def get_all_users(self):
        """This method returns all users """

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            users = cur.fetchall()
            close_connection(conn)
            users_list =[]
            for user in users:
                user_dict = {
                    "user_id":user[0],
                    "email":user[1],
                    "role":user[3]
                }
                users_list.append(user_dict)
            print(users_list)
            return ({
                "Message":"Successful",
                "Users": users_list,
                "status":200
            })
        except (Exception, psycopg2.DatabaseError) as error:
            return jsonify({
            "message":"Could not get all users",
            "status": 400
        })

    def lookup_token(self, token):
        """This method adds a token to blacklist table"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            bearer_token = "Bearer "+ token
            # print(bearer_token)
            cur.execute("SELECT * FROM blacklist WHERE  token = %s",(bearer_token,))
            token_available = cur.fetchone()
            print(token_available)
            close_connection(conn)

            return token_available

        except (Exception ,psycopg2.DatabaseError) as error:
            print("Could not lookup token", error)
            

    def blacklist_token(self, token):
        """This method adds a token to blacklist table"""
        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("INSERT INTO blacklist(token) VALUES(%s)",(token,))
            close_connection(conn)
            
            return jsonify({
            "message":"Successfully logged out",
            "status": 200
        })
        except (Exception ,psycopg2.DatabaseError) as error: 
            print("Could not store token", error)
    
    def get_user_by_id(self, user_id):
        """This method looks up a user from the DB"""

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE user_id = %s",(user_id,))
            user_exists = cur.fetchone()
            close_connection(conn)
            
            return user_exists

        except (Exception ,psycopg2.DatabaseError) as error: 
            print("Could not get user", error)

    def update_role(self, user_id, role):
        """This method sets a user account to Admin"""

        user_exists = self.get_user_by_id(user_id)

        if not user_exists:
            return jsonify({"message":"User not found",
                            "status": 404})
        
        validate_role = self.validate_role(role)
        if not validate_role:
                  return jsonify({"message": "Role can only be admin or attendant",
                            "status": 400})

        try:
            conn = open_connection()
            cur = conn.cursor()
            cur.execute("UPDATE users SET role = %s WHERE user_id = %s RETURNING user_id, username, role", (role, user_id,))
            updated_user = cur.fetchone()
            close_connection(conn)
            user = {
                "User Id": updated_user[0],
                "Email": updated_user[1],
                "Role": updated_user[2]
            }
            
            return jsonify({"message":"User updated",
                            "User updated": user,
                            "status": 200})

        except (Exception ,psycopg2.DatabaseError) as error: 
            print("Could not update user details", error)