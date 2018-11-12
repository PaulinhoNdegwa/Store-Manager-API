from db.db_config import open_connection, close_connection
import psycopg2
from psycopg2 import Error
from werkzeug.security import generate_password_hash
create_tables_queries = [
    """CREATE TABLE IF NOT EXISTS users(
        user_id SERIAL NOT NULL,
        username VARCHAR PRIMARY KEY NOT NULL,
        password VARCHAR NOT NULL,
        role VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS categories(
        id SERIAL PRIMARY KEY NOT NULL,
        cat_name VARCHAR NOT NULL,
        cat_desc VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS products(
        product_id SERIAL PRIMARY KEY NOT NULL,
        product_name VARCHAR NOT NULL,
        product_model VARCHAR NOT NULL,
        cat_id INT NULL references categories(id),
        unit_price INT NOT NULL,
        quantity INT NOT NULL,
        min_quantity INT NOT NULL,
        created_by VARCHAR references users(username)
    )""",
    """CREATE TABLE IF NOT EXISTS sales(
        sale_id SERIAL PRIMARY KEY NOT NULL,
        product_id INT NOT NULL references products(product_id) ON DELETE\
         RESTRICT,
        total_price INT NOT NULL,
        quantity INT NOT NULL,
        created_by VARCHAR NULL references users(username)
    )""",
    """CREATE TABLE IF NOT EXISTS blacklist(
        id SERIAL PRIMARY KEY NOT NULL,
        token VARCHAR NOT NULL
    )""",
    """CREATE TABLE IF NOT EXISTS carts(
        cart_id SERIAL PRIMARY KEY NOT NULL,
        product_id INT NOT NULL references products(product_id) ON DELETE\
         RESTRICT,
        total_price INT NOT NULL,
        quantity INT NOT NULL,
        new_quantity INT NOT NULL,
        created_by VARCHAR NULL references users(username)
    )"""
]

drop_tables_queries = [
    """DROP TABLE IF EXISTS users CASCADE""",
    """DROP TABLE IF EXISTS products CASCADE""",
    """DROP TABLE IF EXISTS sales CASCADE""",
    """DROP TABLE IF EXISTS blacklist CASCADE""",
    """DROP TABLE IF EXISTS categories CASCADE""",
    """DROP TABLE IF EXISTS cart CASCADE"""

]

admin_password = generate_password_hash("Qwerty1")


def create_tables():
    """Function to create new tables for test instance"""
    try:
        conn = open_connection()
        cur = conn.cursor()

        for q in create_tables_queries:
            cur.execute(q)
        cur.execute("SELECT * FROM users WHERE username = 'admin@gmail.com'")
        admin = cur.fetchone()
        if not admin:
            cur.execute(
                "INSERT INTO users (username, password, role) \
                VALUES ('admin@gmail.com', %s, 'Admin')",
                (admin_password,))

        close_connection(conn)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error creating connect:", error)


def drop_tables():
    """Function to drop all the tables after tests"""

    conn = open_connection()
    cur = conn.cursor()

    for q in drop_tables_queries:
        cur.execute(q)

    close_connection(conn)
