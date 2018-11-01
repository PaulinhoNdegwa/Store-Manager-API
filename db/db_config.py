import psycopg2
import os
from psycopg2 import Error
from Instance.config import app_config


def connect_db():
    """"Establishses connection with DB"""
    config = os.getenv("APP_SETTINGS")
    print(config)
    if config != "testing" and config != "development":
        database_url = "postgres://brtaaikaaglcck:b456c778bf66cd3d1e93bebdbcb0d838b501c4ae995d75e745459a4e36f5aa90@ec2-107-21-93-132.compute-1.amazonaws.com:5432/dd5gg557q2fle4"
    else:
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
