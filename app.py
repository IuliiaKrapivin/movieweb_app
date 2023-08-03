from flask import Flask, render_template, request, redirect, url_for
from datamanager.json_data_manager import JSONDataManager

app = Flask(__name__)
data_manager = JSONDataManager('datamanager/users_data.json')


@app.route('/users')
def list_users():
    users = data_manager.get_all_users()
    return render_template('users.html', users=users)


@app.route('/users/<user_id>')
def list_user_movies(user_id):
    movies_list = data_manager.get_user_movies(user_id)
    return render_template('movies.html', user=movies_list, user_id=user_id)


@app.route('/add_user', methods=['GET', 'POST'])
def add_user():

    if request.method == 'POST':
        user_name = request.form.get('name')
        data_manager.add_user(user_name)
        return redirect(url_for('list_users'))
    return render_template('add_user.html')


@app.route('/users/<user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):

    if request.method == 'POST':
        name = request.form.get('name')
        director = request.form.get('director')
        year = request.form.get('year')
        rating = request.form.get('rating')
        data_manager.add_movie(user_id, name, director, year, rating)
        return redirect(url_for('list_user_movies'))
    return render_template('add_movie.html')


if __name__ == '__main__':
    app.run(debug=True)
