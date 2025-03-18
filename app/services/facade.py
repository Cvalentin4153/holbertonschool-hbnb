from app.persistence.amenity_repository import AmenityRepository
from app.persistence.user_repository import UserRepository
from app.persistence.review_repository import ReviewRepository
from app.persistence.place_repository import PlaceRepository
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, first_name, last_name, email, password, is_admin=False):
        user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            is_admin=is_admin
        )
        user.hash_password(password)
        self.user_repo.add(user)
        return user

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        
        if "first_name" in data:
            user.first_name = user.validate_name(data["first_name"])
        if "last_name" in data:
            user.last_name = user.validate_name(data["last_name"])
        if "email" in data:
            user.email = user.validate_email(data["email"])
        
        self.user_repo.update(user_id, data)
        return user

    def create_place(self, title, description, price, latitude, longitude,owner_id, amenities=None):
        owner = self.user_repo.get(owner_id)
        if not owner:
            raise ValueError("Owner not found.")
        place = Place(title, description, price, latitude, longitude, owner)
        self.place_repo.add(place)
        owner.add_place(place)
        if amenities:
            for amenity_id in amenities:
                amenity_obj = self.amenity_repo.get(amenity_id)
                if amenity_obj:
                    place.add_amenity(amenity_obj)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, data):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        
        # Handle amenities separately
        amenities = data.pop('amenities', None)
        
        # Update other fields
        for key, value in data.items():
            setattr(place, key, value)
            
        # Update amenities if provided
        if amenities is not None:
            place.amenities = []
            for amenity_id in amenities:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)
                    
        from extensions import db
        db.session.commit()
        return place

    def create_review(self, text, rating, user_id, place_id):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User does not exist.")

        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place does not exist.")

        review = Review(text, rating, place, user)
        self.review_repo.add(review)

        place.reviews.append(review)

        return review
    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place.reviews

    def update_review(self, review_id, data):
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")

        if "text" in data:
            review.text = review.validate_comment(data["text"])
        if "rating" in data:
            review.rating = review.validate_rating(data["rating"])

        self.review_repo.update(review_id, data)
        review.save()
        return review

    def delete_review(self, review_id):
        """Delete a review by ID."""
        review = self.review_repo.get(review_id)
        if not review:
            raise ValueError("Review not found.")
        
        # Remove the review from the place's reviews list
        if review.place:
            review.place.reviews.remove(review)
        
        # Delete the review
        self.review_repo.delete(review_id)
        from extensions import db
        db.session.commit()

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

    def link_amenity_to_place(self, place_id: str, amenity_id: str) -> Place:
        """Link an amenity to a place."""
        place = self.place_repo.get(place_id)
        amenity = self.amenity_repo.get(amenity_id)
        if not place or not amenity:
            raise ValueError("Place or Amenity not found.")

        place.amenities.append(amenity)
        from extensions import db
        db.session.commit()
        return place
