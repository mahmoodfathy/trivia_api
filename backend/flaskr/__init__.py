import sys,os

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS,cross_origin
import random
from models import setup_db, Question, Category


QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
  questions_page = request.args.get('page',1,type=int)
  start = (questions_page-1)*QUESTIONS_PER_PAGE
  end = start+QUESTIONS_PER_PAGE
  questions = [question.format() for question in selection]
  return questions[start:end]

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}},supports_credentials=True)
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers','Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods','GET,POST,PATCH,PUT,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route('/api/categories')
  def get_categories():
    categories = Category.query.all()
    result_category = {}
    for category in categories:
      format_category = category.format()
      result_category[format_category['id']]=format_category['type']


    if len(categories)==0:
      abort(404)
    return jsonify({
     'success':True,
      'categories':result_category,
      'code':200
    })

  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/api/questions")
  def get_questions():
    selection = Question.query.all()
    paginated_questions = paginate_questions(request,selection)
    categories = Category.query.all()
    result_category = {}
    for category in categories:
      format_category = category.format()
      result_category[format_category['id']] = format_category['type']
    if len(paginated_questions)==0:
      abort(404)
    return jsonify({
      'questions':paginated_questions,
      'total_questions':len(selection),
      'categories':result_category,
      'current_category':None, #categories[0].format()
      'success':True,
      'code':200
      })

  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route('/api/questions/<int:id>',methods=["DELETE"])
  def delete_question(id):
    question = Question.query.get(id)
    if question:
      question.delete()
    else:
      abort(404)
    return jsonify({
      'success':True,
      'code':200
    })

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route('/api/questions',methods=["POST"])

  def create_question():
    body = request.get_json()
    question = body.get('question')
    answer = body.get('answer')
    category= body.get('category')
    difficulty =body.get('difficulty')
    if not ('question' in body and 'answer' in body and 'difficulty' in body and 'category' in body):
      abort(422)
    try:

      inserted_question = Question(question=question,difficulty=difficulty,answer=answer,category=category)
      inserted_question.insert()
    except:
      abort(422)

    finally:
      return jsonify({
        'success': True,
        'code': 200
      })






  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route('/api/questions/search',methods=['POST'])
  def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm')
    if search_term:
      res = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
      questions = [question.format() for question in res]
      return jsonify({
        'success':True,
        'code':200,
        'questions':questions,
        'total_questions':len(res)
      })

    else:
      abort(404)

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route('/api/categories/<int:id>/questions')
  def get_byId(id):
    #modified query to stringify the id cause it was failing in testcases but worked in development wwithout it
    res=Question.query.filter(Question.category==str(id)).all()
    questions=[question.format() for question in res]
    if len(res)==0:
      abort(404)
    return jsonify({
      'success':True,
      'code':200,
      'current_category':res[0].category,
      'total_questions':len(res),
      'questions':questions
    })


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
  @app.route('/api/quizzes',methods=['POST'])
  def play():
    body=request.get_json()
    quiz_category=body.get('quiz_category')
    previous_questions = body.get('previous_questions')

    if quiz_category['id']=='1':
      #notin filter from documentaion https://docs.sqlalchemy.org/en/13/orm/tutorial.html
      science_questions = Question.query.filter(Question.category==1).filter(~Question.id.in_(previous_questions)).all()
      if not science_questions:
        abort(404)
      choice=random.choice(science_questions).format()
      return jsonify({
        'question': choice,
        'success':True,
        'code':200

      })
    elif quiz_category['id']=='2':
      art_questions =  Question.query.filter(Question.category==2).filter(~Question.id.in_(previous_questions)).all()
      if not art_questions:
        abort(404)
      choice = random.choice(art_questions).format()
      return jsonify({
        'question': choice,
        'success':True,
        'code':200
      })
    elif quiz_category['id']=='3':
      geography_questions =  Question.query.filter(Question.category==3).filter(~Question.id.in_(previous_questions)).all()
      if not geography_questions:
        abort(404)
      choice = random.choice(geography_questions).format()
      return jsonify({
        'question': choice,
        'success': True,
        'code': 200
      })
    elif quiz_category['id']=='4':
      history_questions=Question.query.filter(Question.category==4).filter(~Question.id.in_(previous_questions)).all()
      if not history_questions:
        abort(404)
      choice = random.choice(history_questions).format()
      return jsonify({
        'question': choice,
        'success': True,
        'code': 200
      })
    elif quiz_category['id'] == '5':
      Entertainment_questions = Question.query.filter(Question.category == 5).filter(
        ~Question.id.in_(previous_questions)).all()
      if not Entertainment_questions:
        abort(404)
      choice = random.choice(Entertainment_questions).format()
      return jsonify({
        'question': choice,
        'success': True,
        'code': 200
      })
    elif quiz_category['id'] == '6':
      sports_questions = Question.query.filter(Question.category == 6).filter(
        ~Question.id.in_(previous_questions)).all()
      if not sports_questions:
        abort(404)
      choice = random.choice(sports_questions).format()
      return jsonify({
        'question': choice,
        'success': True,
        'code': 200
      })
    else:
      all_questions=Question.query.filter(~Question.id.in_(previous_questions)).all()
      if not all_questions:
        abort(404)
      choice = random.choice(all_questions).format()
      return jsonify({
        'question': choice,
        'success': True,
        'code': 200
      })

      #print(choice.format())



  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success':False,
      'code':404,
      'message':'resource not found!'
    }),404

  @app.errorhandler(422)
  def not_found(error):
    return jsonify({
      'success': False,
      'code': 422,
      'message': 'unprocessable!'
    }), 422

  
  return app

    