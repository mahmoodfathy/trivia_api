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
        self.database_path = "postgresql://postgres:{}@{}/{}".format('mahmoodfathy','localhost:5432', self.database_name)
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

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_notFound_route(self):
        res = self.client().get('/anime')
        data = json.loads(res.data)
        self.assertEqual(data['code'],404)
        self.assertEqual(data['success'],False)
        self.assertEqual(data['message'],'resource not found!')
    def test_get_paginated_questions(self):
        res = self.client().get("/api/questions")
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    def test_categories(self):
        res = self.client().get('/api/categories')
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['code'],200)
        self.assertTrue(data['categories'])
    def test_get_non_existing_category(self):
        res = self.client().get('/api/categories/8000')
        data = json.loads(res.data)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found!')
    def test_deleting_questions(self):
        question = Question(question='how to work test',answer='unitest',difficulty=1,category=1)
        question.insert()
        res = self.client().delete(f'/api/questions/{question.id}')
        data = json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['code'],200)
    def test_deleting_nonexisting_question(self):
        res=self.client().delete('/api/questions/90')
        data=json.loads(res.data)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found!')
    def test_question_creation(self):
        no_questions_before = len(Question.query.all())
        res = self.client().post('/api/questions',json={
            'question':"how to make tests?",
            'answer': 'unitest',
            'difficulty': 1,
            'category':1
        })
        data = json.loads(res.data)
        no_question_after = len(Question.query.all())
        self.assertEqual(data['success'],True)
        self.assertEqual(data['code'],200)
        self.assertEqual(no_question_after,no_questions_before+1)
    def test_creating_question_with_missing_body(self):
        res = self.client().post('/api/questions', json={
            'question': "how to make tests?",
            'answer': 'unitest',
        })
        data = json.loads(res.data)
        self.assertEqual(data['code'], 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable!')
    def test_searching_functionality(self):
        res=self.client().post('/api/questions/search',json={'searchTerm':'a'})
        data=json.loads(res.data)
        self.assertEqual(data['success'],True)
        self.assertEqual(data['code'],200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
    def test_none_existing_question_search(self):
        res=self.client().post('/api/questions/search',json={'searchTerm':''})
        data = json.loads(res.data)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found!')
    def test_get_questions_by_category_id(self):
        res= self.client().get(f"/api/categories/1/questions")
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['code'], 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['current_category'])
    def test_non_existing_category_id(self):
        res = self.client().get(f"/api/categories/10/questions")
        data = json.loads(res.data)
        self.assertEqual(data['code'], 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found!')
    def test_play(self):
        res = self.client().post('/api/quizzes',json={'previous_questions':[],'quiz_category':{'id':1,'type':'science'}})
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['code'], 200)
        self.assertTrue(data['question'])
















# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()