import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from sqlalchemy import exc

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={"/": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        '''
        Sets access control.
        '''
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    @app.route('/')
    def hello():
        '''
        Test Api.
        '''
        return jsonify({
            'message': "Hello, welcome to Capstone project"
            })

    # get all the actors
    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actor.query.all()
            formatted_actors = [actor.format() for actor in actors]
        except Exception as e:
            abort(422)

        return jsonify({"success": True, "actors": formatted_actors})

    # get all the movies
    @app.route('/movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movie.query.all()
            formatted_movies = [movie.format() for movie in movies]
        except Exception as e:
            abort(422)

        return jsonify({"success": True, "movies": formatted_movies})

    # create new actor
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def post_actors(payload):
        try:
            indata = json.loads(request.data)
            name = indata['name']
            age = indata['age']
            gender = indata['gender']

            actor = Actor(name=name, age=age, gender=gender)
            actor.insert()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "actor": actor.format()})

    # create new movie
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def post_movies(payload):
        try:
            indata = json.loads(request.data)
            title = indata['title']
            release_date = indata['release_date']

            movie = Movie(title=title, release_date=release_date)
            movie.insert()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "movie": movie.format()})

    # update actor details
    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, actor_id):

        indata = json.loads(request.data)

        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        try:
            name = indata.get('name')
            age = indata.get('age')
            gender = indata.get('gender')

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            actor.update()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "actor": actor.format()})

    # update movie details
    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movies(payload, movie_id):

        indata = json.loads(request.data)

        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        try:
            title = indata.get('title')
            release_date = indata.get('release_date')

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            movie.update()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "movie": movie.format()})

    # delete actor
    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, actor_id):
        actor = Actor.query.get(actor_id)
        if actor is None:
            abort(404)
        try:
            actor.delete()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "delete": actor_id})

    # delete movie
    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, movie_id):
        movie = Movie.query.get(movie_id)
        if movie is None:
            abort(404)
        try:
            movie.delete()
        except Exception as e:
            abort(400)

        return jsonify({"success": True, "delete": movie_id})

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unauthorized'
        }), 401

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)
