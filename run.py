from app import create_app

config = "development"
if __name__ == "__main__":
    storemanager = create_app(config)
    storemanager.run(debug=True)

# from app import storemanager

# if __name__ == "__main__":
#     storemanager.run(debug=True)