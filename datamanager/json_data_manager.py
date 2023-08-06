import json
import requests
from datamanager.data_manager_interface import DataManagerInterface

KEY = '34571e1b'


class JSONDataManager(DataManagerInterface):
    """Class created to perform operations with users data stored in JSON file"""
    def __init__(self, filename):
        self.filename = filename

    def get_all_users(self):
        """Function uploads all users from JSON file and returns it as a list"""
        try:
            with open(self.filename, "r") as fileobject:
                users_list = json.loads(fileobject.read())
                return users_list
        except IOError as e:
            print("An IOError occurred: ", str(e))

    def get_user_movies(self, user_id):
        """Function uploads all user movies from JSON file and returns it as a list"""
        users_list = self.get_all_users()
        for user in users_list:
            for key in user.keys():
                if key == user_id:
                    # Return all the movies for a given user
                    return user[f'{user_id}']['movies']

    def add_user(self, user_name):
        """Function takes new username as parameter, creates
           and adds a new user dictionary to the JSON file"""
        users_list = self.get_all_users()
        id_list = [int(us_id) for user in users_list for us_id in user.keys()]
        try:
            user_id = max(id_list) + 1  # assigns a unique id to new user
        except ValueError:
            user_id = 1  # if id list is empty will be assigned 1
        new_user = {f"{user_id}": {"name": user_name, "movies": []}}
        users_list.append(new_user)
        json_str = json.dumps(users_list)  # write updated users list to the file
        with open(self.filename, "w") as new_file_object:
            new_file_object.write(json_str)

    def update_movies_list(self, user_id, changed_movie_list):
        """Function rewrites updated movie list for given user to the file"""
        users_list = self.get_all_users()
        for user in users_list:
            for key in user.keys():
                if key == user_id:
                    user[f'{user_id}']['movies'] = changed_movie_list
        json_str = json.dumps(users_list)
        with open(self.filename, "w") as new_file_object:
            new_file_object.write(json_str)

    def add_movie(self, user_id, name):
        """Function takes new movie name and user id as parameters, searches for movie by sending request
        to the API, takes movie data from response and adds a new movie data to exact user movies list"""
        user_movies = self.get_user_movies(user_id)
        id_list = [int(val) for movie in user_movies for key, val in movie.items() if key == "id"]
        try:
            movie_id = max(id_list) + 1  # assigns a unique id to new movie
        except ValueError:
            movie_id = 1  # if id list is empty will be assigned 1
        # making a request with movie name
        try:
            url = f'https://www.omdbapi.com/?apikey={KEY}&t={name}'
            response = requests.get(url)
            data = response.json()  # saves the response
            # filters the response
            name = data['Title']
            year = data['Year']
            rating = float(data['Ratings'][0]['Value'][:-3])
            director = data['Director']
            # creating a new movie record
            new_movie = {'id': movie_id, 'name': name, 'director': director, 'year': year, 'rating': rating}
            user_movies.append(new_movie)
        except KeyError:
            print("Movie is not found")  # prints an error message if movie wasn't found
        except requests.exceptions.ConnectionError:
            print("Connection issue")  # prints an error message if connection problem is appeared
        except IndexError:  # prints an error message if rating format is in unexpected format
            print("Rating format not supported")
        # writes updated movie list to the storage
        self.update_movies_list(user_id, user_movies)

    def update_movie(self, user_id, movie_id, name, director, year, rating):
        """Function takes exact movie data and user id as parameters, searches for movie in the storage,
        updates and saves movie record with provided data"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:  # searching for exact movie by provided id
                movie['name'] = name
                movie['director'] = director
                movie['year'] = year
                movie['rating'] = rating
        # writes updated movie list to the storage
        self.update_movies_list(user_id, user_movies)

    def delete_movie(self, user_id, movie_id):
        """Function takes movie id and user id as parameters to find and delete exact movie from the storage"""
        user_movies = self.get_user_movies(user_id)
        for movie in user_movies:
            if movie['id'] == movie_id:  # searching for exact movie by provided id
                user_movies.remove(movie)
        # writes updated movie list to the storage
        self.update_movies_list(user_id, user_movies)
