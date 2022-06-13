import os
# from os.path import join, dirname
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flaskr import create_app
from models import setup_db, Question, Category
# from dotenv import load_dotenv
# dotenv_path = join(dirname(__file__), '.env')
# load_dotenv(dotenv_path)

DB_HOST = os.getenv('DB_HOST')
DB_TEST_USER = os.getenv('DB_TEST_USER')
DB_TEST_PASSWORD = os.getenv('DB_TEST_PASSWORD')
DB_NAME_TEST = os.getenv('DB_NAME_TEST')

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = DB_NAME_TEST
        # postgresql://{DB_TEST_USER}:{DB_TEST_PASSWORD}@{DB_HOST}/{self.database_name}
        self.database_path = "postgresql://{}:{}@{}/{}".format(DB_TEST_USER,DB_TEST_PASSWORD,DB_HOST, self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

            self.new_question = {
                'question': 'Which was the best marvel movie?',
                'answer': 'Iron man -1',
                'category': 1,
                'difficulty': 3,
            }
    
    def tearDown(self):
        """Executed after reach test"""
        pass


    # def invalidpage(self):
    #     # '''
    #     # Will get total questions and get the total pages possible then checking for result of page+1
    #     # '''
    #     total_questions = len(Question.query.all())
    #     total_page = (total_questions/10)+1
    #     response = self.client.get(
    #         f'/api/v1/questions?page={total_page}')
    #     data = json.loads(response.data)
    #     self.assertEqual(response.status_code, 404)    
    #     self.assertEqual(data['message'], 'resource not found')

    def test_get_categories(self):
        '''
        Checking for the category (in this question it will return all the categories)
        '''
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
         
    
# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()