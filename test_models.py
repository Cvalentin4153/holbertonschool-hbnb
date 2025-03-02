from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

# Create a user
user = User("John", "Doe", "john.doe@example.com")

# Create a place
place = Place("Cozy Apartment", "A nice place", 120, 37.7749, -122.4194, user)

# Create a review
review = Review("Great stay!", 5, place, user)
place.add_review(review)

# Create an amenity
wifi = Amenity("Wi-Fi")
place.add_amenity(wifi)

print("All tests passed!")
