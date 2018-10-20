
products = []
sales = []
users = []


class User():
    """This class initialized a user object. 
    Also it has a save method that saves the user in a list"""

    def __init__(self):
        pass

    def save_user(self, email, password, role="attendant"):
        
        user_id = len(users) + 1
        user = {
            "user_id": user_id,
            "email": email,
            "password": password,
            "role": role
        }
        users.append(user)
        return user    

    def get_user(self, username):

        user_exist = [user for user in users if username == user["username"]]
        if user_exist:
            return True
        return False