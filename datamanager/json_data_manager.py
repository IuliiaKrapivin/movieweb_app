import json
from datamanager.data_manager_interface import DataManagerInterface


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
                    # Return all the movies for a given user
                    return user[f'{user_id}']['movies']

    def add_user(self, user_name):
        users_list = self.get_all_users()
        id_list = [int(us_id) for user in users_list for us_id in user.keys()]
        try:
            user_id = max(id_list) + 1  # assigns a unique id to new user
        except ValueError:
            user_id = 1
        new_user = {f"{user_id}": {"name": user_name, "movies": []}}
        users_list.append(new_user)
        json_str = json.dumps(users_list)
        with open(self.filename, "w") as new_file_object:
            new_file_object.write(json_str)

    def add_movie(self, user_id, name, director, year, rating):
        user_movies = self.get_user_movies(user_id)
        id_list = [int(val) for movie in user_movies for key, val in movie.items() if key == "id"]
        try:
            movie_id = max(id_list) + 1  # assigns a unique id to new movie
        except ValueError:
            movie_id = 1
        new_movie = {'id': movie_id, 'name': name, 'director': director, 'year': year, 'rating': rating}
        user_movies.append(new_movie)

        users_list = self.get_all_users()
        for user in users_list:
            print(user)
            for key in user.keys():
                print(key)
                print(user_id)
                if key == user_id:
                    print(user[f'{user_id}']['movies'])
                    user[f'{user_id}']['movies'] = user_movies
        json_str = json.dumps(users_list)
        with open(self.filename, "w") as new_file_object:
            new_file_object.write(json_str)






