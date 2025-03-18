from .repository import SQLAlchemyRepository
from app.models.amenity import Amenity
from extensions import db

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    def add(self, amenity):
        db.session.add(amenity)
        db.session.commit()
        return amenity

    def get(self, amenity_id):
        return Amenity.query.get(amenity_id)

    def get_all(self):
        return Amenity.query.all()

    def update(self, amenity_id, data):
        amenity = self.get(amenity_id)
        if amenity:
            for key, value in data.items():
                setattr(amenity, key, value)
            db.session.commit()
        return amenity

    def delete(self, amenity_id):
        amenity = self.get(amenity_id)
        if amenity:
            db.session.delete(amenity)
            db.session.commit()
        return amenity