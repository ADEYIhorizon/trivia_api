import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    # CORS(app, resources={r"*/api/*": {origins: '*'}})
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response
    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
   """
    @app.route('/categories')
    def get_categories():
        categories = Category.query.all()
        if len(categories) == 0:
            abort(404)

        result = []
        for category in categories:
            result.append(
                {
                    "id": category.id,
                    "type": category.type
                }
            )
        return jsonify({
            'success':True,
            'Categories': result
        })
            
    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        questions = Question.query.all()
        categories = Category.query.all()

        list_category = [i.type for i in categories]

        
        result = []
        for question in questions:
            result.append(
                {
                    "id": question.id,
                    "question": question.question,
                    # 'difficulty': question.difficulty,
                    'category': question.category,

                }
            )
        return jsonify({
            'success':True,
            'Questions': result[start:end],
            'Total Number of Questions': len(result),
            "categories": list_category
        })



    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route("/questions/<int:question_id>", methods=["DELETE"])
    def delete_question(question_id):
        try:
            question = Question.query.get(question_id)
            # filter_by(Question.id == question_id).one_or_none()

            if question is None:
                abort(404)

            question.delete()
            questions_a = Question.query.all()
            list_questions = [i.format() for i in questions_a]


            return jsonify(
                {
                    "success": True,
                    "deleted": question_id,
                    "Questions": list_questions,
                    "total_questions": len(Question.query.all()),
                }
            )

        except:
            abort(422)


    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route("/questions", methods=["POST"])
    def post_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            record = Question(question=new_question, answer=new_answer,
            category=new_category, difficulty=new_difficulty)
            record.insert()   
            questions_a = Question.query.all()
            list_questions = [i.format() for i in questions_a]

            return jsonify(
                {
                    "success": True,
                    "created": record.id,
                    "Questions": list_questions,
                    "total_questions": len(Question.query.all()),
                }
            )
        except:
            abort(422)

        
    
    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        body = request.get_json()

        search_term = body.get('search_term', None)
        
        try:
            search_result = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            print(search_result)
            if len(search_result) == 0:
                return jsonify({"result": "The search result is empty"})

            response={
                        "count": len(search_result),
                        "data": []
                    }
            print("good")
            for search in search_result:
                response['data'].append({
                    "id": search.id,
                    "name": search.name,
                    "num_upcoming_shows": len(search.upcoming_shows)
                })
            return jsonify(response)
        except:
            abort(404)


    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id>/questions')
    def get_questions_by_categories(id):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        
        questions = Question.query.filter(Question.category == str(id)).all()

        return jsonify({ 
            "Questions" : [i.format() for i in questions],
            "Category": id,
            "Question Count": len(questions)})


    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400


    return app

