from flask import Flask
from flask_restx import Api
from extensions import db
from extensions import bcrypt
from app.api.v1.__init__ import v1_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()
cors = CORS()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": "*"}})
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(v1_bp)

    return app