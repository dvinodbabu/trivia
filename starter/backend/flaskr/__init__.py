import os
from flask import Flask, app, request, abort, jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from model.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 5



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)

  
  def paginate_questions(request, selection):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]
    return current_questions
  
  def formatted_categories():
    formatted_categories = {}
    categories = Category.query.all()
    for category in categories:
      formatted_categories[category.id] = category.type
    return formatted_categories

  @app.route('/categories',  methods=["GET"])
  def categories():
    return jsonify({'categories':formatted_categories()})

  @app.route("/questions", methods=["GET"])
  def questions():
    selection=Question.query.order_by(Question.id).all()
    current_questions=paginate_questions(request,selection)
    if len(current_questions)==0:
      abort(404)
    return jsonify(
      {
        "success": True,
        "questions": current_questions,
        "total_questions": len(Question.query.all()),
        "current_category": None,
        "categories": formatted_categories(),
      }
    )
  @app.route("/questions", methods=["POST"])
  def add_questions():
    try:
      body=request.get_json()
      question=Question(question=body.get("question", None),
      answer=body.get("answer", None),
      difficulty=body.get("difficulty", None),
      category=body.get("category", None))
      question.insert()
      selection = Question.query.order_by(Question.id).all()
      current_questions=paginate_questions(request,selection)
      return jsonify(
         {
           "success" : True,
            "deleted" : question.id,
            "questions" : current_questions,
            "total_questions" : len(Question.query.all())
         }
       )
    except:
      abort(422)
    
  
  @app.route("/questions'/<int:question_id>", methods=["DELETE"])
  def delete_questions(question_id):
     try:
       question = Question.query.filter(Question.id==question_id).one_or_none()
       if question is None:
        abort(404)
       question.delete()
       selection = Question.query.order_by(Question.id).all()
       current_questions=paginate_questions(request,selection)
       return jsonify(
         {
            "success" : True,
            "deleted" : question_id,
            "questions" : current_questions,
            "total_questions" : len(Question.query.all())
         }
       )
     except:
            abort(422)
   
  @app.route("/categories/<int:category_id>/questions", methods=["GET"])
  def get_questions_by_category(category_id):
    question = Question.query.filter(Question.category==category_id).all()
    current_questions=paginate_questions(request,question)
    return jsonify(
      {
        'questions':current_questions,
        'totalQuestions':len(question),
        'current_category':'History'
      }
    )

  @app.after_request
  def after_request(response):
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTION')
   return response
  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  
  return app


    