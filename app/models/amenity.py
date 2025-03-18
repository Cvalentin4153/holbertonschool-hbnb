from app.models.basemodel import BaseModel
from extensions import db
from sqlalchemy.orm import relationship
from app.models.associations import places_amenities, user_amenities


class Amenity(BaseModel):
    __tablename__ = "amenities"

    id = db.Column(db.String(50), primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    places = relationship("Place", secondary=places_amenities, back_populates="amenities")
    users = relationship("User", secondary=user_amenities, back_populates="added_amenities")

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise TypeError("Amenity must be a string of 50 chartacters or less.")
        return name