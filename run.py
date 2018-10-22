from app import create_app

config = "development"
storemanager = create_app(config)

if __name__ == "__main__":
    storemanager.run()
