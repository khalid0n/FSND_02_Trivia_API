import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}@{}/{}".format('khalednasser', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            'question': 'ttt00',
            'answer': 'ansttttt000',
            'difficulty': 4,
            'category': '2'
        }

        self.failure_question = {
            'question2': '',
            'answer': 'ansttttt000',
            'difficulty': 4,
            'category': '2'
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_all_categries(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_paginated_questions_success(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(len(data['questions']))

    def test_get_paginated_questions_failed(self):
        response = self.client().get('/questions?page=1111')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)

    def test_delete_question(self):
        response = self.client().delete('/questions/13')
        data = json.loads(response.data)

        question = Question.query.filter(Question.id == 13).one_or_none()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 13)
        self.assertEqual(question, None)

    def test_delete_question_fail(self):
        response = self.client().delete('/questions/15')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertFalse(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_create_new_question(self):
        response = self.client().post('/add', json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_question_fail(self):
        response = self.client().post('/add', json=self.failure_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 422)

    def test_get_questions_with_search(self):
        response = self.client().post('/questions/search', json={'searchTerm': 'What movie earned Tom Hanks his third straight Oscar nomination, in 1996?'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['totalQuestions'])
        self.assertEqual(data['totalQuestions'], 1)


    def test_get_questions_with_search_fail(self):
        response = self.client().post('/questions/se', json={'searchTerm': 'kgl.dlfgl.dsfd'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
