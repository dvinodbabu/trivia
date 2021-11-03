import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from model.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgres://{}:{}@{}/{}".format('vinod', 'password', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_paginated_questions(self):
        
        response = self.client().get('/questions')
        result = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        print(result['total_questions'])
        # check that total_questions and questions return data
        self.assertTrue(result['total_questions'])
        self.assertTrue(result(data['questions']))

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()