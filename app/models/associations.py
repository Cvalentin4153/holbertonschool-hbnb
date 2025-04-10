from extensions import db
from app.models.basemodel import BaseModel

user_amenities = db.Table(
    "user_amenities",
    BaseModel.metadata,
    db.Column("user_id", db.String(50), db.ForeignKey("users.id"), primary_key=True),
    db.Column("amenity_id", db.String(50), db.ForeignKey("amenities.id"), primary_key=True),
)

places_amenities = db.Table(
    "places_amenities",
    BaseModel.metadata,
    db.Column("place_id", db.String(50), db.ForeignKey("places.id"), primary_key=True),
    db.Column("amenity_id", db.String(50), db.ForeignKey("amenities.id"), primary_key=True)
)

user_reviews = db.Table(
    "user_reviews",
    BaseModel.metadata,
    db.Column("user_id", db.String(50), db.ForeignKey("users.id"), primary_key=True),
    db.Column("review_id", db.String(50), db.ForeignKey("reviews.id"), primary_key=True)
)

places_reviews = db.Table(
    "places_reviews",
    BaseModel.metadata,
    db.Column("place_id", db.String(50), db.ForeignKey("places.id"), primary_key=True),
    db.Column("review_id", db.String(50), db.ForeignKey("reviews.id"), primary_key=True)
)