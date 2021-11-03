
# Imports

import os
from flask import Flask, app, request, abort, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from model.models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 5


# paginate questions set QUESTIONS_PER_PAGE to the desired value
def paginate_questions(request, selection):
    """
    Paginate the list of questions that is displayed in the browser
    Default value is 5 per page.
    Args:
      request: flask request object
      selection: total list of questions
    Returns:
      questions: paginated list of questions

    """
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
# format categories as per the spec


def formatted_categories():
    """
    Method used to format the categories in the below format
    'categories': { '1' : "Science",
    '2' : "Art",
    '3' : "Geography",
    '4' : "History",
    '5' : "Entertainment",
    '6' : "Sports" }
    Args:

    Returns:
      Category: dictionary of formated categories

    """
    formatted_categories = {}
    categories = Category.query.all()
    for category in categories:
        formatted_categories[category.id] = category.type
    return formatted_categories


def create_app(test_config=None):
    """ create app method, sets the db and CORS related configuration
    Args:

    Returns:

    """
    app = Flask(__name__)
    setup_db(app)
    cors = CORS(app, resources={
                r"/*": {"origins": "*"}}, supports_credentials=True)

    # Get list of categories from db

    @app.route('/categories', methods=["GET"])
    def categories():
        """
        Method used to get list of categories from the 'trivia' db.
        HTTP: GET

        Args:

        Returns:
         Category: dictionary of formated categories

        """
        return jsonify({'categories': formatted_categories()})

    # Get list of questions from db - supports pagination

    @app.route('/questions', methods=["GET"])
    def questions():
        """
        Method used to get list of questions from the 'trivia' db.
        HTTP:GET

        Args:

        Returns:
         JSON :
         {
          "success":
          "questions":
          "total_questions":
          "current_category":
          "categories":
          }
        """
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)
        if len(current_questions) == 0:
            abort(404)
        return jsonify({
            "success": True,
            "questions": current_questions,
            "total_questions": len(Question.query.all()),
            "current_category": None,
            "categories": formatted_categories(), }
        )

    # Add a new question in db

    @app.route("/questions", methods=["POST"])
    def add_questions():
        """
        Method used to add a new questions from the 'trivia' db.
        The values of 'question', 'answer', 'difficulty' and 'category' comes
        as json
        from the request from consuming service.
        HTTP:POST

        Args:

        Returns:

        """
        try:
            body = request.get_json()
            question = Question(question=body.get("question", None), answer=body.get(
                "answer", None), difficulty=body.get(
                "difficulty", None), category=body.get("category", None))
            question.insert()
        # selection = Question.query.order_by(Question.id).all()
        # current_questions=paginate_questions(request,selection)
        except:
            abort(422)

    # delete a question from db
    @app.route("/questions'/<int:question_id>", methods=["DELETE"])
    def delete_questions(question_id):
        """
        Method used to delete a existing questions from the 'trivia' db.
        HTTP:DELETE
        Args:
         int : question_id of the question to be deleted
        Returns:
         JSON :
          {
         "success":
         "deleted":
         "questions":
         "total_questions":
          }
        """
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            if question is None:
                abort(404)
            question.delete()
            selection = Question.query.order_by(Question.id).all()
            current_questions = paginate_questions(request, selection)
            return jsonify({
                "success": True,
                "deleted": question_id,
                "questions": current_questions,
                "total_questions": len(Question.query.all())}
            )
        except:
            abort(422)

    # Get list of questions from db by category- supports pagination

    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        """
        Method used to get a list of existing questions from the
        'trivia' db by category
        HTTP:GET
        Args:
         int : category_id of the category for which the questions have
               to be displayed
        Returns:
         JSON :
          {
           "questions":
           "total_questions":
           "current_category":
          }
         """
        question = Question.query.filter(
            Question.category == category_id).all()
        current_questions = paginate_questions(request, question)
        current_category = db.session.query(Category.type).filter(
            Category.id == category_id).all()
        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(question),
            'current_category': current_category}
        )

    # search a question by wild card from list of questions in db

    @app.route("/questions/query", methods=["POST"])
    def question_search():
        """
        Method used to get a search for existing questions from the 'trivia'
        db by user given search term
        HTTP:POST
        Args:
         JSON : searchTerm
        Returns:
         JSON :
         {
          "questions":
          "total_questions":
          "current_category":
         }
        """
        wild_search_question_name = "%{}%".format(
            request.get_json().get('searchTerm', None))
        selection = Question.query.filter(
            Question.question.ilike(wild_search_question_name)).all()
        current_questions = paginate_questions(request, selection)
        return jsonify({
            'questions': current_questions,
            'totalQuestions': len(selection),
            'current_category': None}
        )

    # start quiz - display random set of questions by category

    @app.route("/quizzes", methods=["POST"])
    def start_quiz():
        """
        Method used to display questions by the selected category of the
        user. The questions are random and will not be repeated.

        Args:
         JSON : category_id, previous set of questions
        Returns:
         JSON :
          {
            "success":
            "previousQuestions":
            "currentQuestion":
           }
         """
        form = request.get_json()
        previous_questions = form.get('previous_questions')
        category = form.get('quiz_category').get('id')
        if category == 0:
            questions = Question.query.all()
        else:
            questions = Question.query.filter(
                Question.category == category).all()
        for question in questions:
            if question.id not in previous_questions:
                ask_question = question.format()

        return jsonify({
            'success': True,
            'previousQuestions': previous_questions,
            'currentQuestion': ask_question.format()}
        )

    @app.after_request
    def after_request(response):
        """
        Method will be called after the request and adds the below paramteres
        in the response headers.
        Access-Control-Allow-Headers=Content-Type, Authorization
        Access-Control-Allow-Methods=GET, POST, PATCH, DELETE, OPTION
        Args:

        Returns:

        """
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET, POST, PATCH, DELETE, OPTION')
        return response

    return app
