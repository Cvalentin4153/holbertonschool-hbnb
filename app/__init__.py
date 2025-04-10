from flask import Flask
from flask_restx import Api
from extensions import db
from extensions import bcrypt
from app.api.v1.__init__ import v1_bp
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

jwt = JWTManager()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Disable strict slashes
    app.url_map.strict_slashes = False
    
    # Initialize extensions
    bcrypt.init_app(app)
    db.init_app(app)
    jwt.init_app(app)
    
    # Configure CORS
    app.config['CORS_HEADERS'] = 'Content-Type'
    CORS(app, 
         resources={
             r"/api/*": {
                 "origins": ["http://127.0.0.1:3000", "http://localhost:3000"],
                 "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                 "allow_headers": ["Content-Type", "Authorization"],
                 "supports_credentials": True
             }
         })
    
    migrate = Migrate(app, db)
    
    # Register blueprints
    app.register_blueprint(v1_bp)

    return app