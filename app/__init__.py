from flask import Flask
from flask_restx import Api
from app.api.v1.__init__ import v1_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(v1_bp)

    return app