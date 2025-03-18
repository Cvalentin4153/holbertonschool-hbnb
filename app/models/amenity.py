from app.models.basemodel import BaseModel
from extensions import db

class Amenity(BaseModel):
    __tablename__ = "amenity"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __init__(self, name):
        super().__init__()
        self.name = self.validate_name(name)

    def validate_name(self, name):
        if not isinstance(name, str) or len(name) > 50:
            raise TypeError
        ("Amenity must be a string of 50 chartacters or less.")
        return name