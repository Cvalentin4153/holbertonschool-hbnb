import unittest
import requests
import uuid

class TestRelationships(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001/api/v1"

    def setUp(self):
        """Set up test data."""
        # Create a test user
        user_payload = {
            "first_name": "Test",
            "last_name": "User",
            "email": f"test_{uuid.uuid4().hex[:6]}@example.com",
            "password": "test_password123"
        }
        user_resp = requests.post(f"{self.BASE_URL}/users/", json=user_payload)
        self.assertEqual(user_resp.status_code, 201, user_resp.text)
        self.user_id = user_resp.json()["id"]

        # Create a test place
        place_payload = {
            "title": "Test Place",
            "description": "A place for testing relationships",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_resp = requests.post(f"{self.BASE_URL}/places/", json=place_payload)
        self.assertEqual(place_resp.status_code, 201, place_resp.text)
        self.place_id = place_resp.json()["id"]

        # Create a test amenity
        amenity_payload = {"name": f"WiFi_{uuid.uuid4().hex[:6]}"}
        amenity_resp = requests.post(f"{self.BASE_URL}/amenities/", json=amenity_payload)
        self.assertEqual(amenity_resp.status_code, 201, amenity_resp.text)
        self.amenity_id = amenity_resp.json()["id"]

    def test_place_owner_relationship(self):
        """Test the relationship between a place and its owner."""
        # Get place details
        place_resp = requests.get(f"{self.BASE_URL}/places/{self.place_id}")
        self.assertEqual(place_resp.status_code, 200, place_resp.text)
        place_data = place_resp.json()
        
        # Verify owner information is included
        self.assertIn("owner", place_data)
        self.assertEqual(place_data["owner"]["id"], self.user_id)

    def test_place_amenity_relationship(self):
        """Test linking and retrieving amenities for a place."""
        # Link amenity to place
        link_resp = requests.post(
            f"{self.BASE_URL}/places/{self.place_id}/amenities/{self.amenity_id}"
        )
        self.assertEqual(link_resp.status_code, 200, link_resp.text)

        # Get place details to verify amenity is linked
        place_resp = requests.get(f"{self.BASE_URL}/places/{self.place_id}")
        self.assertEqual(place_resp.status_code, 200, place_resp.text)
        place_data = place_resp.json()
        
        # Verify amenities list contains the linked amenity
        self.assertIn("amenities", place_data)
        self.assertEqual(len(place_data["amenities"]), 1)
        self.assertEqual(place_data["amenities"][0]["id"], self.amenity_id)
        self.assertTrue(place_data["amenities"][0]["name"].startswith("WiFi_"))

    def test_place_review_relationship(self):
        """Test creating and retrieving reviews for a place."""
        # Create a review
        review_payload = {
            "text": "Great place!",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        review_resp = requests.post(f"{self.BASE_URL}/reviews/", json=review_payload)
        self.assertEqual(review_resp.status_code, 201, review_resp.text)
        review_id = review_resp.json()["id"]

        # Get place details to verify review is linked
        place_resp = requests.get(f"{self.BASE_URL}/places/{self.place_id}")
        self.assertEqual(place_resp.status_code, 200, place_resp.text)
        place_data = place_resp.json()
        
        # Verify reviews list contains the created review
        self.assertIn("reviews", place_data)
        self.assertEqual(len(place_data["reviews"]), 1)
        self.assertEqual(place_data["reviews"][0]["id"], review_id)

    def test_user_places_relationship(self):
        """Test retrieving all places owned by a user."""
        # Create another place for the same user
        place_payload = {
            "title": "Second Place",
            "description": "Another place owned by the same user",
            "price": 200,
            "latitude": 40.7128,
            "longitude": -74.0060,
            "owner_id": self.user_id,
            "amenities": []
        }
        place_resp = requests.post(f"{self.BASE_URL}/places/", json=place_payload)
        self.assertEqual(place_resp.status_code, 201, place_resp.text)

        # Get user's places
        user_places_resp = requests.get(f"{self.BASE_URL}/users/{self.user_id}/places")
        self.assertEqual(user_places_resp.status_code, 200, user_places_resp.text)
        places_data = user_places_resp.json()
        
        # Verify user has two places
        self.assertEqual(len(places_data), 2)
        place_titles = [place["title"] for place in places_data]
        self.assertIn("Test Place", place_titles)
        self.assertIn("Second Place", place_titles)

    def test_place_update_with_amenities(self):
        """Test updating a place with new amenities."""
        # Create another amenity
        amenity_payload = {"name": "Pool"}
        amenity_resp = requests.post(f"{self.BASE_URL}/amenities/", json=amenity_payload)
        self.assertEqual(amenity_resp.status_code, 201, amenity_resp.text)
        new_amenity_id = amenity_resp.json()["id"]

        # Update place with new amenities
        update_payload = {
            "amenities": [self.amenity_id, new_amenity_id]
        }
        update_resp = requests.put(
            f"{self.BASE_URL}/places/{self.place_id}",
            json=update_payload
        )
        self.assertEqual(update_resp.status_code, 200, update_resp.text)

        # Verify place has both amenities
        place_resp = requests.get(f"{self.BASE_URL}/places/{self.place_id}")
        self.assertEqual(place_resp.status_code, 200, place_resp.text)
        place_data = place_resp.json()
        
        self.assertEqual(len(place_data["amenities"]), 2)
        amenity_names = [amenity["name"] for amenity in place_data["amenities"]]
        self.assertIn("WiFi", amenity_names)
        self.assertIn("Pool", amenity_names)

    def test_place_review_validation(self):
        """Test validation rules for place reviews."""
        # Test invalid rating
        review_payload = {
            "text": "Invalid rating",
            "rating": 6,  # Rating should be between 1 and 5
            "user_id": self.user_id,
            "place_id": self.place_id
        }
        review_resp = requests.post(f"{self.BASE_URL}/reviews/", json=review_payload)
        self.assertEqual(review_resp.status_code, 400, review_resp.text)

        # Test review for non-existent place
        review_payload = {
            "text": "Invalid place",
            "rating": 5,
            "user_id": self.user_id,
            "place_id": "non-existent-id"
        }
        review_resp = requests.post(f"{self.BASE_URL}/reviews/", json=review_payload)
        self.assertEqual(review_resp.status_code, 404, review_resp.text)

if __name__ == "__main__":
    unittest.main() 