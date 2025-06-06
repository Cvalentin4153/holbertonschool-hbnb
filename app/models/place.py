from __future__ import annotations
from typing import TYPE_CHECKING
from app.models.basemodel import BaseModel
from app.models.amenity import Amenity
from app.models.associations import places_amenities, places_reviews
from extensions import db
from datetime import datetime
from sqlalchemy.orm import relationship

if TYPE_CHECKING:
    from app.models.review import Review
    from app.models.user import User


class Place(BaseModel):
    __tablename__ = "places"

    id = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, default=0)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    owner_id = db.Column(db.String(50), db.ForeignKey("users.id"), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    owner = relationship("User", back_populates="places")
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=places_amenities, back_populates="places")
    place_reviews = relationship("Review", secondary=places_reviews, back_populates="reviewed_places")

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = self.validate_title(title)
        self.description = description
        self.price = self.validate_price(price)
        self.latitude = self.validate_latitude(latitude)
        self.longitude = self.validate_longitude(longitude)
        self.owner = self.validate_owner(owner)
        self.reviews = []
        self.amenities = []

    def validate_title(self, title):
        if not isinstance(title, str):
            raise TypeError("Title must be a string.")
        return title

    def validate_price(self, price):
        if not isinstance(price, (int, float)) or price < 0:
            raise ValueError("Price must be a positive number.")
        return price

    def validate_latitude(self, latitude):
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90.")
        return latitude

    def validate_longitude(self, longitude):
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180.")
        return longitude

    def validate_owner(self, owner: "User"):
        from app.models.user import User
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")
        return owner

    def add_review(self, review: "Review"):
        from app.models.review import Review
        if not isinstance(review, Review) or review.place == self:
            self.reviews.append(review)
        else:
            raise ValueError("Invalid review.")

    def add_amenity(self, amenity):
        if not isinstance(amenity, Amenity) and amenity not in self.amenities:
            self.amenities.append(amenity)

    def validate_description(self, description):
        if not isinstance(description, str):
            raise TypeError("Description must be a string.")
        return description