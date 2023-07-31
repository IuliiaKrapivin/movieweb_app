import json
from data_manager_interface import DataManagerInterface


class JSONDataManager(DataManagerInterface):
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        with open(self.filename, "r") as fileobject:
            users_list = json.loads(fileobject.read())
            return users_list

    def get_user_movies(self, user_id):
        users_list = self.get_all_users()
        for user in users_list:
            for key in user.keys():
                if key == user_id:
                    return user[f'{user_id}']['movies']
        # Return all the movies for a given user


# list_users = JSONDataManager("users_data.json")
# print(list_users.get_user_movies("2"))