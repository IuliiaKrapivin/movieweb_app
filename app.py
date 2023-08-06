from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager


app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users_data.json')


@app.route('/users')
def list_users():
    """Route renders main page template with all users"""
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    """Route renders page template with all movies for chosen user"""
    try:
        movies_list = data_manager.get_user_movies(user_id)
        return render_template('movies.html', user=movies_list, user_id=user_id)
    except TypeError:
        return "User with this id doesn't exist"


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Route renders page template with form for adding new user"""
    if request.method == 'POST':
        user_name = request.form.get('name')
        if user_name == '':
            return "User name is empty"
        data_manager.add_user(user_name)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    """Route renders page template with form for adding new movie for chosen user"""
    try:
        if request.method == 'POST':
            name = request.form.get('name')
            if name == '':
                return "Movie name is empty"
            data_manager.add_movie(user_id, name)
            return redirect(url_for('list_user_movies', user_id=user_id))
        return render_template('add_movie.html', user_id=user_id)
    except TypeError:
        return "User with this id doesn't exist"


@app.route('/users/<user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    """Route renders page template with form for updating chosen movie for chosen user"""
    try:
        user_movies = data_manager.get_user_movies(user_id)  # returns all user movies
        for movie in user_movies:
            if movie['id'] == movie_id:  # searching for exact movie by provided id
                if request.method == 'POST':  # update the movie data if new data sent
                    name = request.form.get('name')
                    director = request.form.get('director')
                    year = request.form.get('year')
                    rating = request.form.get('rating')
                    data_manager.update_movie(user_id, movie_id, name, director, year, rating)
                    return redirect(url_for('list_user_movies', user_id=user_id))
                return render_template('update_movie.html', movie=movie, movie_id=movie_id, user_id=user_id)
        return "Movie with this id doesn't exist"
    except TypeError:
        return "User with this id doesn't exist"


@app.route('/users/<user_id>/delete_movie/<int:movie_id>')
def delete_movie(user_id, movie_id):
    """Route for deleting chosen movie for chosen user"""
    try:
        data_manager.delete_movie(user_id, movie_id)
        return redirect(url_for('list_user_movies', user_id=user_id))
    except TypeError:
        return "User or movie with this id doesn't exist"


@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@app.errorhandler(405)
def method_not_allowed_error(error):
    return render_template('405.html'), 405


if __name__ == '__main__':
    app.run(debug=True)
