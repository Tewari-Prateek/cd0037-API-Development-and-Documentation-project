import random
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def pagination(request, question_data):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in question_data]
    selected_questions = questions[start:end]

    return selected_questions


def create_app():
    app = Flask(__name__)
    setup_db(app)

    """
    Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/*": {"origins": "*"}})
    """
    Use the after_request decorator to set Access-Control-Allow
    """
    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    @app.route("/questions/")
    def get_questions():
        question_data = Question.query.order_by(Question.id).all()
        formatted_categories = {
            question_category.id: question_category.type
            for question_category in Category.query.all()}
        selected_questions = pagination(request, question_data)

        if len(selected_questions) == 0:
            abort(404)
        return jsonify(
            {
                'success': True,
                'questions': selected_questions,
                'totalQuestions': len(question_data),
                'categories': formatted_categories,
                'currentCategory': 'all',
            }
        )

    @app.route("/categories")
    def retrieve_categories():
        return jsonify({
            'success': True,
            'categories': {
                            question_category.id: question_category.type
                            for question_category in Category.query.all()}})

    @app.route("/categories/<id>")
    def retrieve_categories_bad_request(id):
        abort(422)

    @app.route("/categories/<int:cat_id>/questions")
    def get_questions_for_category(cat_id):
        if Category.query.get(cat_id) is None:
            abort(404)
        questions = Question.query.filter_by(category=cat_id).all()
        return jsonify({
            'success': True,
            'questions': [q.format() for q in questions],
            'totalQuestions': len(questions),
            'currentCategory': Category.query.get(cat_id).type
        }
        )

    @app.route("/questions/<int:id>", methods=["DELETE"])
    def delete_question(id):
        question = Question.query.get(id)
        if question is None:
            abort(404)
        try:
            question.delete()
            updated_questions = Question.query.all()
            return jsonify({
                'success': True,
                'questions': pagination(request, updated_questions),
                'totalQuestions': len(updated_questions),
                'categories': {
                    question_category.id: question_category.type
                    for question_category in Category.query.all()},
                'currentCategory': 'all',
            }
            )
        except:
            abort(422)

    @app.route("/questions", methods=["POST"])
    def post_question_add_and_search():
        body = request.get_json()
        add_question = body.get("question", None)
        add_answer = body.get("answer", None)
        add_difficulty = body.get("difficulty", None)
        add_category = body.get("category", None)
        searchTerm = body.get("searchTerm", None)

        if searchTerm:
            question_data = Question.query.order_by(Question.id).filter(
                Question.question.ilike("%{}%".format(searchTerm))
            )
            matching_questions = pagination(request, question_data)
            return jsonify({
                'success': True,
                'questions': matching_questions,
                'totalQuestions': len(question_data.all()),
                'currentCategory': 'all',
            })
            
        elif add_question and add_answer and add_difficulty and add_category:
            question = Question(
                question=add_question, category=add_category,
                answer=add_answer, difficulty=add_difficulty)
            question.insert()
            return jsonify(
                {
                    'success': True,
                    'question': add_question,
                    'answer': add_answer,
                    'difficulty': add_difficulty,
                    'category': add_category,
                    'created': question.id
                }
            )
        else:
            abort(422)

    @app.route("/quizzes", methods=["POST"])
    def post_quiz():
        body = request.get_json()
        previous_questions = body.get("previous_questions", None)
        quiz_category = body.get("quiz_category", None)
        if quiz_category['id']:
            questions_not_already_asked = Question.query.filter(
                Question.category == quiz_category['id']).filter(
                ~Question.id.in_(previous_questions)).all()
        else:
            questions_not_already_asked = Question.query.filter(
                ~Question.id.in_(previous_questions)).all()
        if questions_not_already_asked:
            new_question = random.choice(questions_not_already_asked)
        else:
            new_question = None

        return jsonify({
            'success': True,
            'question': new_question.format() if new_question else None
        })

    @app.errorhandler(400)
    def bad_request(e):
        return jsonify({'success': False,
                        'message': 'Bad Request'}), 400

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({'success': False,
                        'message': 'Resource not found'}), 404
    
    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "success": False, "error": 405, 'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(e):
        return jsonify({'success': False,
                        'message': 'Unprocessable Entity'}), 422

    @app.errorhandler(500)
    def internal_server_error(e):
        return jsonify({'success': False,
                        'message': 'Internal Server Error'}), 500

    return app
