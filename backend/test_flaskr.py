import os
from os.path import join, dirname
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
from dotenv import load_dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

DB_HOST = os.environ.get('DB_HOST')
DB_TEST_USER = os.environ.get('DB_TEST_USER')
DB_TEST_PASSWORD = os.environ.get('DB_TEST_PASSWORD')
DB_TEST_NAME = os.environ.get('DB_TEST_NAME')


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_TEST_NAME
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            DB_TEST_USER, DB_TEST_PASSWORD, DB_HOST, self.database_name)

        setup_db(self.app, self.database_path)

        # self.new_question = {"question": "Who's the author of the book 'Steve Jobs' published in 2013 and 2015?",
        #                      "answer": "Walter Isaacson", "difficulty": 3, "category": 4}
        # self.previous_questions = [17, 22]

       # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                "question": "The first man to swim across the Palk straits is?",
                "answer": "Mihir Sen", "difficulty": 5, "category": 6
            }

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_categories(self):
        
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_post_question(self):
        '''
        Adding the question and checking for the response from the request
        '''
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)
        
        self.assertTrue(res.status_code, 200)
        self.assertTrue(data['success'])

    def test_get_quiz(self):
       
        quiz_round = {'previous_questions': [], 'quiz_category': {
            'type': 'All', 'id': 0}}
        res = self.client().post('/quizzes', json=quiz_round)
        data = json.loads(res.data)

        # check status code and success message
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_page_not_found(self):
        '''
        Will get total questions and get the total pages possible then checking for result of page+1
        '''
        total_questions = len(Question.query.all())
        total_page = (total_questions/10)+1
        response = self.client().get(
            f'/api/v1/questions?page={total_page}')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'Resource not found')


    def test_valid_search_term(self):
      '''
       Checking for search term functionality
      '''
      res = self.client().post('/questions', json={'searchTerm': 'swim'})
      data = json.loads(res.data)
    
      self.assertEqual(res.status_code, 200)
      self.assertTrue(data['questions'])
      self.assertTrue(data['totalQuestions'])


    def test_invalid_search_term(self):
        '''
    Checking for search term functionality (if search result is not pressent then return)
    '''
        res = self.client().post('/questions', json={"searchTerm": "Shaktimaan"})
        data = json.loads(res.data)
        self.assertEqual(data['questions'], [])
        self.assertEqual(data['totalQuestions'], 0)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
