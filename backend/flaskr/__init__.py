from flask import Flask, request, abort, jsonify
from flask_cors import CORS, cross_origin
from flask.helpers import send_from_directory
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, static_folder="../frontend/build", static_url_path='')
    setup_db(app)
    CORS(app, resources={r"/api/*" : {'origins': '*'}})

    #cors headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Allow-Control-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Allow-Control-Methods', 'POST, GET, PATCH, DELETE')

        return response

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]

        return current_questions

    @app.route('/')
    @cross_origin
    def serve():
        return send_from_directory(app.static_folder, 'index.html')
    
    @app.route('/categories', methods=['GET'])
    def get_categories():
        try:
            categories = Category.query.all()

            return jsonify({
                'success' : True,
                'categories' : {category.id : category.type for category in categories}
            })
        except Exception as e:
            print(e)
            abort(400)
    
    @app.route('/questions', methods=['GET'])
    def get_questions():
        try:
            selection = Question.query.all() 
            current_questions = paginate_questions(request, selection)
            categories = Category.query.order_by(Category.type).all()  

            if len(current_questions) == 0:
                abort(404)

            return jsonify({
                'success' : True,
                'questions' : current_questions,
                'totalQuestions' : len(selection),
                'categories' : {category.id : category.type for category in categories},
                'currentCategory' : ''
            })
        except Exception as e:
            print(e)
            abort(404)

    @app.route('/questions/<int:id>', methods=['DELETE'])
    def delete_question(id):
        try:
            question = Question.query.filter(Question.id == id).one_or_none()

            if question is None:
                abort(404)
            
            question.delete()

            return jsonify({
                'success' : True,
                'deleted' : question.id,
            })
        except Exception as e:
            print(e)
            abort(422)            

    @app.route('/questions', methods=['POST'])
    def post_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_difficulty = body.get('difficulty', None)
        new_category = body.get('category', None)

        try:
            question = Question(question=new_question, answer=new_answer, difficulty=new_difficulty, category=new_category)
            question.insert()

            selection = Question.query.all()
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                    abort(404)

            return jsonify({
                'success' : True,
                'created' : question.id,
                'questions' : current_questions,
                'totalQuestions' : len(selection),
                'currentCategory' : ''
            })
        except:
            abort(422)

    @app.route('/questions/search', methods=['POST'])
    def search_question():
        body = request.get_json()

        searchTerm = body.get('searchTerm', None)

        try:
            selection = Question.query.order_by(Question.id).filter(Question.question.ilike(f'%{searchTerm}%'))
            current_questions = paginate_questions(request, selection)

            if len(current_questions) == 0:
                    abort(404)

            return jsonify({
                    'success' : True,
                    'questions' : current_questions,
                    'totalQuestions' : len(current_questions),
                    'currentCategory' : ''
            })
        except Exception as e:
            print(e)
            abort(404)


    @app.route('/categories/<int:id>/questions', methods=['GET'])
    def get_questions_categories(id):
        try:
            if id > 6:
                abort(400)
            questions = Question.query.filter(Question.category == id).all()
            formatted_questions = [question.format() for question in questions]

            category = Category.query.filter(Category.id == id).first()

            return jsonify({
                'success' : True,
                'questions' : formatted_questions,
                'totalQuestions' : len(Question.query.all()),
                'currentCategory' : category.type
            })
        except:
            abort(400)

    
    @app.route('/quizzes', methods=['POST'])
    def get_questions_to_play():
        body = request.get_json()

        previous_questions = body.get('previous_questions', None)
        quiz_category = body.get('quiz_category', None)

        try:
            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter(Question.category == quiz_category['id']).all()
            
            current_questions = [question.format() for question in questions]
            next_question = random.choice(current_questions)

            if len(previous_questions) == len(current_questions):
                next_question = None
            return jsonify({
                'success' : True,
                'question' : next_question
            })
        except:
            abort(422)


    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success' : False,
            'error' : 404,
            'message' : 'resource not found' 
        }), 404
    
    @app.errorhandler(422)
    def unproccesable(error):
        return jsonify({
            'success' : False,
            'error' : 422,
            'message' : 'unprocessable'
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success' : False,
            'error' : 400,
            'message' : 'bad request'
        }), 400
    
    
    return app

