import os
from flask import Flask, app, request, abort, jsonify,json
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from model.models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 5



def create_app(test_config=None):
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
    current_category=db.session.query(Category.type).filter(Category.id==category_id).all()
    return jsonify(
      {
        'questions':current_questions,
        'totalQuestions':len(question),
        'current_category': current_category
      }
    )

  @app.route("/questions/query" ,methods=["POST"])
  def question_search():
    wild_search_question_name = "%{}%".format(request.get_json().get('searchTerm', None))
    selection = Question.query.filter(Question.question.ilike(wild_search_question_name)).all()
    current_questions=paginate_questions(request,selection)
    return jsonify(
      {
        'questions':current_questions,
        'totalQuestions':len(selection),
        'current_category': None
      }
    )

  @app.route("/quizzes", methods=["POST"])
  def start_quiz():
    form=request.get_json()
    previous_questions = form.get('previous_questions')
    category = form.get('quiz_category').get('id')
    print(category)
    if category==0:
      questions = Question.query.all()
    else:
      questions = Question.query.filter(Question.category==category).all()
    for question in questions:
     if question.id not in previous_questions:
      ask_question=question.format()

    return jsonify({
      'success':True,
      'previousQuestions':previous_questions,
      'currentQuestion':ask_question.format()
    })

  @app.after_request
  def after_request(response):
   response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
   response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTION')
   return response


  return app


    