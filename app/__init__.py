from flask import Flask
from flask_restx import Api
from app.api.v1.users import user_ns
from app.api.v1 import v1_bp

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    app.register_blueprint(v1_bp)

    return app