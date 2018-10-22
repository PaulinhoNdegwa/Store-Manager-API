
products = []
sales = []
users = []


class User():
    """This class initialized a user object. 
    Also it has a save method that saves the user in a list"""

    def __init__(self, f_name, s_name, email, password, role="attendant"):
        self.f_name = f_name
        self.s_name = s_name
        self.email = email
        self.password = password
        self.role = role

    def save_user(self):
        if len(users) == 0:
            user_id = 1
        else:
            user_id = users[-1]["user_id"] + 1
        user = {
            "user_id": user_id,
            "f_name": self.f_name,
            "s_name": self.s_name,
            "email": self.email,
            "password": self.password,
            "role":self.role
        }
        users.append(user)
        return user    
