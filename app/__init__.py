"""
Return the app after creating our function
"""

from flask import Flask, jsonify, Blueprint

# local imports
from app.api.v2.admin.routes import path_2 as meetups
from app.api.v2.questions.routes import path_2 as questions
from app.api.v2.users.routes import path_2 as users
from app.admin.db import init_db

from config import app_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.register_blueprint(meetups)
    app.register_blueprint(questions)
    app.register_blueprint(users)
    
    # register database url
    init_db(app_config["DB_URL"])
    # Register error handlers

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': 'Bad request. Check the syntax', 'status': 400}), 400
        
    @app.errorhandler(404)
    def page_not_found(error):
        return jsonify({'error': 'Url not found', 'status': 404}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({'error': 'Method not allowed', 'status': 405}), 405

    return app