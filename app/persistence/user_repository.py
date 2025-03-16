from app.models import User
from extensions import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def get_user_by_id(self, id):
        return self.model.query.filter_by(id=id).first()