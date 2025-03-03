import unittest
from app.services.facade import HBnBFacade
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

class TestFacade(unittest.TestCase):
    def setUp(self):
        """Create a fresh facade for each test."""
        self.facade = HBnBFacade()

        # Optionally seed with sample data
        self.user = self.facade.create_user("John", "Doe", "john.doe@example.com")
        self.place = self.facade.create_place(
            title="Test Place",
            description="A place for testing",
            price=100,
            latitude=37.7749,
            longitude=-122.4194,
            owner_id=self.user.id,
        )
        self.amenity = self.facade.create_amenity("Wi-Fi")

    def test_create_user(self):
        """Test creating a new user via facade."""
        user_count_before = len(self.facade.user_repo.get_all())
        new_user = self.facade.create_user("Alice", "Smith", "alice@example.com")
        user_count_after = len(self.facade.user_repo.get_all())

        self.assertEqual(user_count_before + 1, user_count_after)
        self.assertEqual(new_user.first_name, "Alice")

    def test_create_place(self):
        """Test creating a place and ensuring owner is linked."""
        place_count_before = len(self.facade.place_repo.get_all())
        new_place = self.facade.create_place(
            title="Another Place",
            description="Just another test place",
            price=200,
            latitude=40.7128,
            longitude=-74.0060,
            owner_id=self.user.id
        )
        place_count_after = len(self.facade.place_repo.get_all())

        self.assertEqual(place_count_before + 1, place_count_after)
        self.assertEqual(new_place.owner, self.user)

    def test_create_review(self):
        """Test review creation references existing user & place."""
        review_count_before = len(self.facade.review_repo.get_all())
        review = self.facade.create_review(
            text="Great stay!",
            rating=5,
            user_id=self.user.id,
            place_id=self.place.id
        )
        review_count_after = len(self.facade.review_repo.get_all())

        self.assertEqual(review_count_before + 1, review_count_after)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.place, self.place)


    def test_create_amenity(self):
        """Test creating an amenity."""
        amen_count_before = len(self.facade.amenity_repo.get_all())
        amen = self.facade.create_amenity("Parking")
        amen_count_after = len(self.facade.amenity_repo.get_all())

        self.assertEqual(amen_count_before + 1, amen_count_after)
        self.assertEqual(amen.name, "Parking")

if __name__ == "__main__":
    unittest.main()
