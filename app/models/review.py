from __future__ import annotations
from typing import TYPE_CHECKING
from app.models.basemodel import BaseModel

if TYPE_CHECKING:
    from app.models.place import Place
    from app.models.user import User

class Review(BaseModel):
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