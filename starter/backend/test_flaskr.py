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
        self.question = {
            'question' : 'What is the capial of Scotland',
            'answer' : 'Edinburgh',
            'difficulty': 3,
            'category' : 3
        }
        self.searchTerm={
            'searchTerm': 'penicillin'
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

    def test_paginated_questions(self):
        
        response = self.client().get('/questions')
        result = json.loads(response.data)
        # check status code and message
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        #print(result['total_questions'])
        # check that total_questions and questions return data
        self.assertTrue(result['total_questions'])
        self.assertTrue(result['questions'])
    
    def test_list_of_categories(self):
        response = self.client().get('/categories')
        result = json.loads(response.data)
        print(len(result['categories']))
        self.assertEqual(response.status_code,200)
        self.assertEqual(len(result['categories']),6)
        
    def test_add_question(self):
        current_questions_number = len(Question.query.all())
        response = self.client().post('/questions', json=self.question)
        result = json.loads(response.data)
        latest_questions_number=len(Question.query.all())
        print(current_questions_number, latest_questions_number)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertEqual(current_questions_number, latest_questions_number-1)      

    def test_delete_question(self):
        response = self.client().delete('/questions/39')    
        result = json.loads(response.data)
        latest_questions_list=Question.query.all()
        print(len(latest_questions_list))
        self.assertEqual(result['success'], True)

    def test_select_questions_by_category(self):
        response = self.client().get('/categories/2/questions')
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)

    def test_search_question_by_wild_card(self):
        response = self.client().post('/questions/query', json=self.searchTerm)
        result = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result['success'], True)
        self.assertEqual(result['totalQuestions'],1)

        
        
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
