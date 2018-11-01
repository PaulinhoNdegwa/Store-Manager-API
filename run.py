from app import create_app
from db import tables


tables.create_tables()
config = "development"
storemanager = create_app(config)

if __name__ == "__main__":
    storemanager.run()
