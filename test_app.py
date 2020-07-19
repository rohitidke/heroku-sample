import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Actor, Movie

from dotenv import load_dotenv
load_dotenv()


class CapstoneTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.casting_assistant = os.environ['CASTING_ASSISTANT']
        self.casting_director = os.environ['CASTING_DIRECTOR']
        self.executive_producer = os.environ['EXECUTIVE_PRODUCER']

        setup_db(self.app)

        # sample actor and movie for use in tests
        self.new_actor = {
            'name': 'Sushant singh Rajput',
            'age': 35,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Dil Bechara',
            'release_date': '2020-07-22'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_create_actors(self):

        # make request and process response
        response = self.client().post(
            '/actors', headers={
                                "Authorization": "Bearer {}".format(
                                 self.casting_director)
                                }, json=self.new_actor)
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_create_movies(self):

        # make request and process response
        response = self.client().post(
            '/movies', headers={
                                "Authorization": "Bearer {}".format(
                                 self.executive_producer)
                                }, json=self.new_movie)
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_create_actors_by_assistant(self):

        # make request and process response
        response = self.client().post(
            '/actors', headers={
                                "Authorization": "Bearer {}".format(
                                 self.casting_assistant)
                                }, json=self.new_actor)
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Doesnt have valid\
         permission to access.')

    def test_create_movies_by_assistant(self):

        # make request and process response
        response = self.client().post(
            '/movies', headers={
                                "Authorization": "Bearer {}".format(
                                 self.casting_assistant)
                                }, json=self.new_movie)
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Doesnt have valid\
         permission to access.')

    def test_update_actors(self):

        # make request and process response
        response = self.client().patch(
            '/actors/1', headers={
                                  "Authorization": "Bearer {}".format(
                                   self.casting_director)
                                }, json={'name': 'Arnold'})
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_update_movies(self):

        # make request and process response
        response = self.client().patch(
            '/movies/1', headers={
                                 "Authorization": "Bearer {}".format(
                                  self.executive_producer)
                                }, json={'title': 'Joker'})
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_update_actors_by_assistant(self):

        # make request and process response
        response = self.client().patch(
            '/actors/3', headers={
                                  "Authorization": "Bearer {}".format(
                                   self.casting_assistant)
                                }, json={'name': 'Arnold'})
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Doesnt have valid\
         permission to access.')

    def test_update_movies_by_assistant(self):

        # make request and process response
        response = self.client().patch(
            '/movies/3', headers={
                                  "Authorization": "Bearer {}".format(
                                   self.casting_assistant)
                                }, json={'title': 'Joker'})
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Doesnt have valid\
         permission to access.')

    def test_get_actors(self):

        # make request and process response
        response = self.client().get('/actors')
        response = self.client().get(
            '/actors', headers={
                                "Authorization": "Bearer {}".format(
                                 self.casting_assistant)
                               })
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies(self):

        # make request and process response
        response = self.client().get(
            '/movies', headers={
                                "Authorization": "Bearer {}".format(
                                 self.casting_assistant)
                                })
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_actors(self):

        # make request and process response
        response = self.client().delete(
            '/actors/2', headers={
                                  "Authorization": "Bearer {}".format(
                                   self.casting_director)
                                 })
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

    def test_delete_movies(self):

        # make request and process response
        response = self.client().delete(
            '/movies/2', headers={
                                  "Authorization": "Bearer {}".format(
                                   self.executive_producer)
                                 })
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)

    def test_delete_movies_by_director(self):

        # make request and process response
        response = self.client().delete(
            '/movies/4', headers={
                                 "Authorization": "Bearer {}".format(
                                  self.casting_director)
                                })
        data = json.loads(response.data)

        # make assertions on the response data
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Doesnt have valid permission\
         to access.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
