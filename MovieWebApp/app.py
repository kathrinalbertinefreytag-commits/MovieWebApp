from flask import Flask, render_template, request, flash, redirect, url_for
from data_manager import DataManager
from models import db, Movie, User
import os


app = Flask(__name__)
data_manager = DataManager()
app.secret_key = os.environ.get("SECRET_KEY", "dev-only-key")

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/movies.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
data_dir = os.path.join(basedir, "data")
os.makedirs(data_dir, exist_ok=True)
db.init_app(app)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/users")
def list_users():
    users = data_manager.get_users()
    return render_template("users.html", users=users)


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    if request.method == "POST":
        name = request.form.get("name")

        if not name:
            flash("User name is required")
        else:
            data_manager.create_user(name)
            flash("User created successfully!")
            return redirect(url_for("list_users"))

    return render_template("create_user.html")

@app.route("/users/<int:user_id>/movies/add", methods=["POST"])
def add_movie_to_user(user_id):
    title = request.form.get("title")
    if not title:
        flash("Movie title is required.", "error")
        return redirect(url_for("movies", user_id=user_id))
    
    try:
        movie = data_manager.create_movie_from_OMDb(title)
        data_manager.add_movie_to_user(user_id, movie.id)
        flash(f"Movie '{movie.title}' added!")
    except ValueError as e:
        flash(str(e), "error")

    return redirect(url_for("movies", user_id=user_id))


@app.route("/users/<int:user_id>/movies")
def movies(user_id):
    user = data_manager.get_user(user_id)
    if not user:
        flash("User not found.")
        return redirect(url_for("list_users"))

    movies = data_manager.get_movies(user_id)
    return render_template(
        "movies.html",
        user=user,          
        movies=movies,
        user_id=user_id
    )


@app.route("/users/<int:user_id>/movies/import", methods=["POST"])
def import_movie(user_id):
    if request.method == "POST":
        title = request.form.get("title")
        if not title:
            flash("Movie title is required", "error")
            return redirect(url_for("movies", user_id=user_id))
        try:
            movie = data_manager.create_movie_from_OMDb(title, user_id)
            flash(f"Movie '{movie.title}' added!")
        except ValueError as e:
            flash(str(e), "error")
        return redirect(url_for("movies", user_id=user_id))
    
    # GET request 
    #return render_template("movies.html")


@app.route('/users/<int:user_id>/movies/<int:movie_id>/update', methods=['POST'])
def update_movie(user_id, movie_id):
    new_title = request.form.get("title")

    if not new_title:
        flash("New title is required")
        return redirect(url_for("movies", user_id=user_id))

    data_manager.update_movie(movie_id, new_title)
    flash("Movie updated successfully!")

    return redirect(url_for("movies", user_id=user_id))

@app.route('/users/<int:user_id>/movies/<int:movie_id>/delete', methods=['POST'])
def delete_movie(user_id, movie_id):
    data_manager.delete_movie(user_id, movie_id)
    flash("Movie deleted from favorites.")
    return redirect(url_for("movies", user_id=user_id))

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
  with app.app_context():
    db.create_all()

  app.run()