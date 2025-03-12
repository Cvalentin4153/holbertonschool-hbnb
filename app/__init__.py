from flask import Flask
from flask_restx import Api
from app.api.v1.__init__ import v1_bp
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.register_blueprint(v1_bp)
    app.config.from_object(config_class)
    bcrypt.init_app(app)


    return app