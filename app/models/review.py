from __future__ import annotations
from typing import TYPE_CHECKING
from app.models.basemodel import BaseModel
from extensions import db
from sqlalchemy.orm import relationship
from app.models.associations import user_reviews, places_reviews

if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.user import User

class Review(BaseModel):
    __tablename__ = "reviews"

    id = db.Column(db.String(50), primary_key=True)
    text = db.Column(db.String(255), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    place_id = db.Column(db.String(50), db.ForeignKey("places.id"), nullable=False)

    place = relationship("Place", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
    reviewers = relationship("User", secondary=user_reviews, back_populates="user_reviews")
    reviewed_places = relationship("Place", secondary=places_reviews, back_populates="place_reviews")

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = self.validate_comment(text)
        self.rating = self.validate_rating(rating)
        self.place = self.validate_place(place)
        self.user = self.validate_user(user)

    def validate_comment(self, text):
        if not isinstance(text, str) or text.strip() == "":
            raise ValueError("Comment can not be empty.")
        return text

    def validate_rating(self, rating):
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            raise ValueError("Rating must be an integer between 1 and 5.")
        return rating

    def validate_place(self, place: "Place"):
        from app.models.place import Place
        if not isinstance(place, Place):
            raise ValueError("Invalid place.")
        return place

    def validate_user(self, user: "User"):
        from app.models.user import User
        if not isinstance(user, User):
            raise ValueError("Invalid user.")
        return user