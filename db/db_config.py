import psycopg2
import os
from psycopg2 import Error


def connect_db():
    """"Establishses connection with DB"""
    # environ = app.config["ENV"]
    database_url = os.getenv("DATABASE_URL_TEST")
    # database_url = environ
    # print(database_url)
    try:
        return psycopg2.connect(database_url)

    except (Exception, psycopg2.DatabaseError) as error:
        print("Could not connect with database", error)


def open_connection():
    "Function to open connection"
    conn = connect_db()
    return conn


def close_connection(conn):
    """Closes connection after queries"""
    conn.commit()
    conn.close()
