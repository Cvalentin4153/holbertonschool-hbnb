from flask import Flask
from flask_restx import Api
from extensions import db
from extensions import bcrypt
from app.api.v1.__init__ import v1_bp
from flask_migrate import Migrate

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.register_blueprint(v1_bp)
    app.config.from_object(config_class)
    bcrypt.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)



    return app