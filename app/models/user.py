import re
from app.models.__init__ import BaseModel
from app.models.place import Place
from app.models.review import Review
from app import db, bcrypt


class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.column(db.String(50), nullable=False)
    last_name = db.column(db.String(50), nullable=False)
    email = db.column(db.String(120), nullable=False, unique=True)
    password = db.column(db.String(128), nullable=False)
    is_admin = db.column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False,):
        super().__init__()
        self.first_name = self.validate_name(first_name)
        self.last_name = self.validate_name(last_name)
        self.email = self.validate_email(email)
        self.is_admin = bool(is_admin)
        self.password = password
        self.places = []
        self.reviews = []

    def validate_name(self, name):
        if not isinstance(name, str):
            raise TypeError(f"{name} must be of type str")
        if not name.strip():
            raise ValueError("Name can not be empty.")
        return name

    def validate_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, email):
            raise ValueError("Invalid email format.")
        return email

    def add_place(self, place):
        if isinstance(place, Place) and place.owner == self:
            self.places.append(place)
        else:
            raise ValueError("Invalid place or owner mismatch.")

    def add_review(self, review):
        if isinstance(review, Review) and review.user == self:
            self.reviews.append(review)
        else:
            raise ValueError("Invalid review or user mismatch.")

def hash_password(self, password):
    """Hashes the password before storing it."""
    self.password = bcrypt.generate_password_hash(password).decode('utf-8')

def verify_password(self, password):
    """Verifies if the provided password matches the hashed password."""
    return bcrypt.check_password_hash(self.password, password)