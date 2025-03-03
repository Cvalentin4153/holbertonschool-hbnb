import unittest
import requests
import uuid

class TestReviewEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001/api/v1/reviews"

    def test_create_review(self):
        """Test POST /api/v1/reviews/ creates a new review."""
        # Create user
        user_payload = {
            "first_name": "ReviewUser",
            "last_name": "Test",
            "email": f"review_{uuid.uuid4().hex[:6]}@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertIn(user_resp.status_code, [200,201], user_resp.text)
        user_id = user_resp.json()["id"]

        # Create place
        place_payload = {
            "title": "Reviewable Place",
            "description": "Place to review",
            "price": 45,
            "latitude": 12.34,
            "longitude": -56.78,
            "owner_id": user_id,
            "amenities": []
        }
        place_resp = requests.post("http://127.0.0.1:5001/api/v1/places/", json=place_payload)
        self.assertIn(place_resp.status_code, [200,201], place_resp.text)
        place_id = place_resp.json()["id"]

        # Create review
        review_payload = {
            "text": "Great place!",
            "rating": 5,
            "user_id": user_id,
            "place_id": place_id
        }
        resp = requests.post(self.BASE_URL + "/", json=review_payload)
        self.assertIn(resp.status_code, [200,201], resp.text)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["text"], "Great place!")
        self.assertEqual(data["rating"], 5)

    def test_get_all_reviews(self):
        """Test GET /api/v1/reviews/ returns list of reviews."""
        resp = requests.get(self.BASE_URL + "/")
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertIsInstance(resp.json(), list)

    def test_update_review(self):
        """Test PUT /api/v1/reviews/<review_id> updates review data."""
        # Create user
        user_payload = {
            "first_name": "ReviewUser2",
            "last_name": "Test2",
            "email": "reviewuser2@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertIn(user_resp.status_code, [200,201], user_resp.text)
        user_id = user_resp.json()["id"]

        # Create place
        place_payload = {
            "title": "Reviewable Place2",
            "description": "Place to review2",
            "price": 99,
            "latitude": 1.1,
            "longitude": -2.2,
            "owner_id": user_id,
            "amenities": []
        }
        place_resp = requests.post("http://127.0.0.1:5001/api/v1/places/", json=place_payload)
        self.assertIn(place_resp.status_code, [200,201], place_resp.text)
        place_id = place_resp.json()["id"]

        # Create review
        review_payload = {
            "text": "Good place",
            "rating": 3,
            "user_id": user_id,
            "place_id": place_id
        }
        rev_resp = requests.post(self.BASE_URL + "/", json=review_payload)
        self.assertIn(rev_resp.status_code, [200,201], rev_resp.text)
        review_id = rev_resp.json()["id"]

        # Update review
        update_payload = {"text": "Updated text", "rating": 4}
        update_url = f"{self.BASE_URL}/{review_id}"
        update_resp = requests.put(update_url, json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["text"], "Updated text")
        self.assertEqual(updated_data["rating"], 4)

    def test_get_reviews_by_place(self):
        """Test GET /api/v1/reviews/places/<place_id>/reviews returns reviews for a place."""
        # Create user
        user_payload = {
            "first_name": "ReviewPlace",
            "last_name": "TestPlace",
            "email": "revplace@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertIn(user_resp.status_code, [200,201], user_resp.text)
        user_id = user_resp.json()["id"]

        # Create place
        place_payload = {
            "title": "ReviewsByPlace",
            "description": "Testing get reviews by place",
            "price": 12,
            "latitude": 3.3,
            "longitude": 4.4,
            "owner_id": user_id
        }
        place_resp = requests.post("http://127.0.0.1:5001/api/v1/places/", json=place_payload)
        self.assertIn(place_resp.status_code, [200,201], place_resp.text)
        place_id = place_resp.json()["id"]

        # Create multiple reviews
        rev_payload_1 = {"text": "Review #1", "rating": 4, "user_id": user_id, "place_id": place_id}
        rev_payload_2 = {"text": "Review #2", "rating": 5, "user_id": user_id, "place_id": place_id}
        requests.post(self.BASE_URL + "/", json=rev_payload_1)
        requests.post(self.BASE_URL + "/", json=rev_payload_2)

        # Get reviews for that place
        get_url = f"{self.BASE_URL}/places/{place_id}/reviews"
        get_resp = requests.get(get_url)
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        data = get_resp.json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 2)

if __name__ == "__main__":
    unittest.main()
