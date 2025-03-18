from .repository import SQLAlchemyRepository
from app.models.review import Review
from extensions import db

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    def add(self, review):
        db.session.add(review)
        db.session.commit()
        return review

    def get(self, review_id):
        return Review.query.get(review_id)

    def get_all(self):
        return Review.query.all()

    def get_by_place(self, place_id):
        return Review.query.filter_by(place_id=place_id).all()

    def update(self, review_id, data):
        review = self.get(review_id)
        if review:
            for key, value in data.items():
                setattr(review, key, value)
            db.session.commit()
        return review

    def delete(self, review_id):
        review = self.get(review_id)
        if review:
            db.session.delete(review)
            db.session.commit()
        return review