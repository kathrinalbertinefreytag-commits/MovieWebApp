from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

user_movie = db.Table(
    "user_movie",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey("movie.id"), primary_key=True)
)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    movies = db.relationship(
        "Movie",
        secondary=user_movie,
        back_populates="users"
    )

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    release_year = db.Column(db.Integer, nullable=True)
    #rating primarily taken from imdb, may be updated by user lateron
    rating = db.Column(db.Float, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    imdb_id = db.Column(db.String(20), unique=True)

    users = db.relationship(
        "User",
        secondary=user_movie,
        back_populates="movies"
    )