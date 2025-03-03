from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, first_name, last_name, email, is_admin=False):
        if self.user_repo.get_by_attribute('email', email):
            raise ValueError("User with the same email already exists.")
        user = User(first_name, last_name, email, is_admin)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found.")

        for key, value in data.items():
            if value:  # Only update non-empty values
                setattr(user, key, value)

        self.user_repo.update(user_id, data)
        return user

    def delete_user(self, user_id):
        if not self.user_repo.get(user_id):
            raise ValueError("User not found.")
        self.user_repo.delete(user_id)

    def create_place(self, title, description, price, latitude, longitude, owner_id):
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found.")
        place = Place(title, description, price, latitude, longitude, owner)
        self.place_repo.add(place)
        owner.add_place(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        place.update(data)
        self.place_repo.update(place_id, data)
        return place

    def delete_place(self, place_id):
        if not self.place_repo.get(place_id):
            raise ValueError("Place not found.")
        self.place_repo.delete(place_id)

    def create_review(self, comment, rating, place_id, user_id):
        place = self.place_repo.get(place_id)
        user = self.user_repo.get(user_id)
        if not place or not user:
            raise ValueError("Place or user not found.")
        review = Review(comment, rating, place, user)
        self.review_repo.add(review)
        place.add_review(review)
        user.add_review(review)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        review.update(data)
        self.review_repo.update(review_id, data)
        return review

    def delete_review(self, review_id):
        if not self.review_repo.get(review_id):
            raise ValueError("Review not found.")
        self.review_repo.delete(review_id)

    def create_amenity(self, name):
        if self.amenity_repo.get_by_attribute('name', name):
            raise ValueError("Amenity already exists.")
        amenity = Amenity(name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            raise ValueError("Amenity not found.")
        amenity.update(data)
        self.amenity_repo.update(amenity_id, data)
        return amenity

    def list_place_amenity(self, place_id, amenity_id):
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)
        if not place or not amenity:
            raise ValueError("Place or amenity not found.")
        place.add_amenity(amenity)