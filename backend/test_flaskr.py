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
        # database_name = 'trivia'
        self.user_name = 'horizon'
        self.pass_word = 'horizon001'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(self.user_name, self.pass_word,'localhost:5432', self.database_name)

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
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_404_category_input_out_of_range(self):
        res = self.client().get('categories/100/questions')
        data = json.loads(res.data)

        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)


    def test_get_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)


        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertEqual(data["current_category"], None)
        self.assertTrue(data["categories"])

    def test_404_unknown_page_numbers(self):
        res = self.client().get('/questions?page=100230')
        data = json.loads(res.data)
        
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        res = self.client().delete("/questions/5")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 5)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["Questions"]))
        self.assertEqual(question, None)

    def test_422_if_question_does_not_exist(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_create_new_question(self):
        self.new_question = {"question": "What is your name", "answer": "Adeyi Q", "category": "5", "difficulty": 10}
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["created"])
        self.assertTrue(data["total_questions"])

    def test_404_if_question_creation_not_allowed(self):
        self.new_question = {"question": "What is your name", "answer": "Adeyi Q", "category": 89, "difficulty": 10}
        res = self.client().post("/questions/45", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "method not allowed")

    def test_search_question(self):
        self.search_term = {"searchTerm": "name"}
        res = self.client().post("/questions/search", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])


    def test_404_invalid_search_term(self):
        self.search_term = {"searchTerm": "hmafmknfnjanjnfj"}
        res = self.client().post("/questions/search", json=self.search_term)
        data = json.loads(res.data)

        self.assertEqual(data['success'], False)
        self.assertEqual(data['error'], 404)
        self.assertEqual(data['message'], "There is no matching question for this search")

    def test_quiz_play(self):
        data_c = {
            'previous_questions':[2, 6],
            'quiz_category': {
                'id': 5,
                'type': 'Entertainment'
            }
        }

        res = self.client().post('/quizzes', json=data_c)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])

        self.assertNotEqual(data['question']['id'], 2)
        self.assertNotEqual(data['question']['id'], 6)

        self.assertEqual(data['question']['category'], 5) 

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()