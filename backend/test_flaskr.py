from decouple import config
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
        self.user = config('USER')
        self.password = config('PASSWORD')
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.user,self.password ,'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
        
        self.new_question = {'question' : 'who created', 'answer' : 'Mark', 'difficulty' : 2, 'category' : 2}
        self.question_category = {'previous_questions': [1, 4, 20, 15], 'quiz_category': {'id' : 1}}
        self.searchTerm = {'searchTerm' : 'who'}
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    
    
    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(len(data['categories']))

    def test_404_request_beyond_existing_page(self):
        res = self.client().get('/questions?page=1000', json={'category' : 4})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_question_delete(self):
        res = self.client().delete('/questions/34')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 34).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 34)
        self.assertEqual(question, None)

    def test_422_if_question_non_existant(self):
        res = self.client().delete('/questions/950')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_create_new_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(len(data['questions']))

    def test_404_question_creation_invalid(self):
        res = self.client().post('/questions/t', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_search_for_questions(self):
        res = self.client().post('/questions/search', json=self.searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_404_search_invalid_search(self):
        res = self.client().post('/questions/search/1', json=self.searchTerm)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    

    def test_get_questions_by_categories(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])

    def test_400_invalid_category(self):
        res = self.client().get('/categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_get_questions_to_play(self):
        res = self.client().post('/quizzes', json=self.question_category)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
    

    def test_422_bad_request_quizzes(self):
        data = {'previous_questions': [], 'quiz_category': {'id' : 100}}
        res = self.client().post('/quizzes', json=data)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()