from datamanager.data_manager_interface import DataManagerInterface
from datamanager.data_models import User, Movie, Review
import requests


KEY = '34571e1b'


class SQLiteDataManager(DataManagerInterface):
    """Class created to perform operations with users data stored in database"""

    def __init__(self, db):
        self.db = db

    def get_all_users(self):
        """Function uploads all users from database and returns it as a list"""
        users = self.db.session.execute(self.db.select(User)).all()
        return users

    def get_user_movies(self, user_id):
        """Function uploads all user movies from database and returns it as a list"""
        movies = self.db.session.execute(self.db.select(Movie).filter(Movie.user == user_id)).all()
        return movies

    def add_user(self, user_name):
        """Function takes new username as a parameter to create new user in database"""
        user = User(user_name=user_name)
        self.db.session.add(user)
        self.db.session.commit()

    def add_movie(self, user_id, name):
        """Function takes new movie name and user id as parameters, searches for movie by sending request
        to the API, takes movie data from response and adds a new movie data to exact user movies list"""
        movies_data = self.db.session.execute(self.db.select(Movie).filter(Movie.user == user_id)).all()
        movies = [movie[0] for movie in movies_data]
        movies_list = [{"movie_name": movie.title, "director": movie.director, "year": movie.year} for movie in movies]
        try:
            url = f'https://www.omdbapi.com/?apikey={KEY}&t={name}'
            response = requests.get(url)
            data = response.json()  # saves the response
            # filters the response
            name = data['Title']
            year = data['Year']
            rating = float(data['Ratings'][0]['Value'][:-3])
            director = data['Director']
            # check if movie is already exist
            for movie in movies_list:
                if movie['movie_name'] == name and int(movie['year']) == int(year) and movie['director'] == director:
                    return "Movie already exist"
            # creating a new movie record
            new_movie = Movie(user=user_id, title=name, director=director, year=year, rating=rating)
            self.db.session.add(new_movie)
            self.db.session.commit()
        except KeyError:
            print("Movie is not found")  # prints an error message if movie wasn't found
        except requests.exceptions.ConnectionError:
            print("Connection issue")  # prints an error message if connection problem is appeared
        except IndexError:  # prints an error message if rating format is in unexpected format
            print("Rating format not supported")

    def update_movie(self, movie_id, name, director, year, rating):
        """Function takes exact movie data as parameters, searches for movie in the storage,
        updates and saves movie record with provided data"""
        movie_to_update = self.db.session.query(Movie).get(movie_id)
        movie_to_update.title = name
        movie_to_update.director = director
        movie_to_update.year = year
        movie_to_update.rating = rating
        self.db.session.commit()

    def delete_movie(self, movie_id):
        """Function takes movie id as a parameter to find and delete exact movie from the storage"""
        self.db.session.execute(self.db.delete(Movie).filter_by(movie_id=movie_id))
        self.db.session.commit()

    def get_movie(self, movie_id):
        """Function takes movie id as a parameter to find and return exact movie"""
        movie = self.db.session.execute(self.db.select(Movie).filter(Movie.movie_id == movie_id)).one()
        # return movie object
        return movie[0]

    def add_review(self, movie_id, text, rating):
        """Function takes movie id and review data to create and save review record to database"""
        new_review = Review(movie_id=movie_id, review_text=text, rating=rating)
        self.db.session.add(new_review)
        self.db.session.commit()

    def get_reviews(self, movie_id):
        """Function returns all reviews to exact movie"""
        reviews = self.db.session.execute(self.db.select(Review).filter(Review.movie_id == movie_id)).all()
        return reviews

    def add_movie_api(self, user_id, title, director, year, rating):
        """Function takes new movie data received from API, creates and saves new movie rec to exact user movies list"""
        new_movie = Movie(user=user_id, title=title, director=director, year=year, rating=rating)
        self.db.session.add(new_movie)
        self.db.session.commit()
