from flask import Blueprint, jsonify, request
from datamanager.sqlite_data_manager import SQLiteDataManager
from datamanager.data_models import db


api = Blueprint('api', __name__)
data_manager = SQLiteDataManager(db)


@api.route('/users', methods=['GET'])
def get_users():
    """Route to retrieve users list"""
    users_data = data_manager.get_all_users()
    users = [user[0] for user in users_data]
    users_list = [{"user_name": user.user_name, "user_id": user.user_id} for user in users]
    return jsonify(users_list)


@api.route('/users/<user_id>/movies', methods=['GET', 'POST'])
def get_movies(user_id):
    """Route to retrieve user movies list (GET request), to create new movie rec (POST request)"""
    if request.method == 'POST':
        new_movie = request.get_json()
        if invalid_post_data(new_movie):
            return jsonify({"error": f"{invalid_post_data(new_movie)}"}), 400
        title = new_movie['title']
        director = new_movie['director']
        rating = new_movie['rating']
        year = new_movie['year']

        data_manager.add_movie_api(user_id, title, director, year, rating)
        return jsonify(new_movie), 201

    else:
        movies_data = data_manager.get_user_movies(user_id)
        movies = [movie[0] for movie in movies_data]
        movies_list = [{"movie_name": movie.title, "director": movie.director, "year": movie.year} for movie in movies]
        return jsonify(movies_list)


def invalid_post_data(data):
    """Function checks new movie input"""
    if 'title' not in data:
        return "title was missed"
    elif 'director' not in data:
        return "director was missed"
    elif 'year' not in data:
        return "year was missed"
    elif 'rating' not in data:
        return "rating was missed"
    return False
