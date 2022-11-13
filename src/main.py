from flask import Flask
from init import db, ma, bcrypt, jwt
from controllers.players_controller import players_bp
from controllers.squad_controller import squad_bp
from controllers.auth_controller import auth_bp
from controllers.cli_controller import db_commands
from marshmallow.exceptions import ValidationError
import os

def create_app():
    app = Flask(__name__)

    # JSON Configuration
    app.config ['JSON_SORT_KEYS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

    # Initialise instances
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    #Register Blueprints
    app.register_blueprint(players_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(db_commands)
    app.register_blueprint(squad_bp)

    # Error Handling
    @app.errorhandler(ValidationError)
    def validation_error(err):
        return {'error': err.messages}, 400

    @app.errorhandler(400)
    def bad_request(err):
        return {'error': str(err)}, 400

    @app.errorhandler(404)
    def not_found(err):
        return {'error': str(err)}, 404

    @app.errorhandler(401)
    def unauthorized(err):
        return {'error': 'You are not authorized to perform this action'}, 401

    @app.errorhandler(KeyError)
    def key_error(err):
        return {'error': f'The field {err} is required.'}, 400

    return app