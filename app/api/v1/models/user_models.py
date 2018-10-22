
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
        """Method returns one user"""

        user_exist = [user for user in users if username == user["username"]]
        return user_exist
        

    def get_all_users(self):
        """This method returns all users """

        return users