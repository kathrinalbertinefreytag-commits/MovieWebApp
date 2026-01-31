from models import db, User, Movie
import os
import requests

class DataManager():
    OMDB_API_KEY = os.environ.get("OMDB_API_KEY")
    OMDB_URL = "http://www.omdbapi.com/"

    def create_user(self, name):
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()

    def get_users(self):
        return User.query.all()
    
    def get_user(self, user_id):
        return User.query.get(user_id)

    
    def get_movies(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return []
        return user.movies
    
    def add_movie_to_user(self, user_id, movie_id):
    
        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)
        
        if not user:
            raise ValueError("User not found.")
        if not movie:
            raise ValueError("Movie not found.")

        if movie not in user.movies:
            user.movies.append(movie)
            db.session.commit()


    def add_movie(self, user_id, title): 
        user = User.query.get(user_id)
        movie = Movie(
            title=data["Title"],
            release_year=int(data["Year"]) if data["Year"].isdigit() else None,
            imdb_id=data["imdbID"],
            rating = parse_rating(data.get("Ratings", []), "Internet Movie Database"),
            imdb_link=self._build_imdb_link(data["imdbID"])
            )
        if not user:
            raise ValueError("User not found.")
        
        if movie not in user.movies:
            user.movies.append(movie)
            db.session.commit()

    def fetch_movie_from_OMDb(self, title):
        params = {"apikey": self.OMDB_API_KEY, "t": title, "type": "movie"}
        response = requests.get(self.OMDB_URL, params=params)
        data = response.json()
        if data.get("Response") == "False":
            raise ValueError(data.get("Error", "Movie not found"))
        return data
    
    def parse_rating(self, ratings, source):
        """
        ratings: List from dictionary, OMDb
        source:  "Internet Movie Database"
        return: float oder None
        """
        Source == "Internet Movie Database"
        for r in ratings:
            if r["Source"] == source:
                value = r["Value"]
                if source == "Internet Movie Database":
                    # "8.8/10" → 8.8
                    return float(value.split("/")[0])
        return None
    
    def _build_imdb_link(self, imdb_id):
        """Generates the IMDb-Link on behalf of imdb_id"""
        if imdb_id:
            return f"https://www.imdb.com/title/{imdb_id}/"
        return None

    def create_movie_from_OMDb(self, title):
        data = self.fetch_movie_from_OMDb(title)
        existing = Movie.query.filter_by(imdb_id=data["imdbID"]).first()
        if existing:
            return existing
        movie = Movie(
            title=data["Title"],
            release_year=int(data["Year"]) if data["Year"].isdigit() else None,
            imdb_id=data["imdbID"],
            rating = parse_rating(data.get("Ratings", []), "Internet Movie Database"),
            imdb_link=self._build_imdb_link(data["imdbID"])
        )
        db.session.add(movie)
        db.session.commit()
        return movie
        

    def update_movie(self, movie_id, new_title=None, new_year=None, new_rating=None):
        movie = Movie.query.get(movie_id)
        if not movie:
            raise ValueError("Movie not found.") 

        if new_title:
            movie.title = new_title
        if new_year:
            movie.release_year = new_year
        if new_rating:
            movie.rating = new_rating
        db.session. commit()
        return movie   

    def delete_movie(self, user_id, movie_id):
        user = User.query.get(user_id)
        movie = Movie.query.get(movie_id)

        if not user or not movie:
            raise ValueError("User or Movie not found")

        if movie in user.movies:
            user.movies.remove(movie)
            db.session.commit()

    
    @staticmethod
    def parse_rating(ratings, source):
        for r in ratings:
            if r["Source"] == source:
                value = r["Value"]
                if source == "Internet Movie Database":
                    return float(value.split("/")[0])
        return None
 
