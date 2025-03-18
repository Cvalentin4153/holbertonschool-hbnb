from .repository import SQLAlchemyRepository
from app.models.place import Place
from extensions import db


class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
    def add(self, place):
        db.session.add(place)
        db.session.commit()
        return place

    def get(self, place_id):
        return Place.query.get(place_id)

    def get_all(self):
        return Place.query.all()

    def update(self, place_id, data):
        place = self.get(place_id)
        if place:
            for key, value in data.items():
                setattr(place, key, value)
            db.session.commit()
        return place

    def delete(self, place_id):
        place = self.get(place_id)
        if place:
            db.session.delete(place)
            db.session.commit()
        return place