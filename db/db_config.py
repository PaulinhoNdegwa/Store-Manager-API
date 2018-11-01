import psycopg2
import os
from psycopg2 import Error
from Instance.config import app_config


def connect_db():
    """"Establishses connection with DB"""
    config = os.getenv("APP_SETTINGS")
    print(config)
    if config != "testing" or config != "development":
        database_url = os.environ['DATABASE_URL'], sslmode = 'require'
    database_url = app_config[config].DATABASE_URL

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
