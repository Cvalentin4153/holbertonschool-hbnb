import unittest
import requests

class TestPlaceEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001/api/v1/places"

    def test_create_place(self):
        """Test POST /api/v1/places/ creates a new place."""
        # First, we need an owner user
        user_payload = {
            "first_name": "PlaceOwner",
            "last_name": "Tester",
            "email": "placeowner@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertEqual(user_resp.status_code, 201, user_resp.text)
        owner_id = user_resp.json()["id"]

        place_payload = {
            "title": "Cozy Apartment",
            "description": "A nice place to stay",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": owner_id,
            "amenities": []  # or some amenity IDs if available
        }
        resp = requests.post(self.BASE_URL + "/", json=place_payload)
        self.assertEqual(resp.status_code, 201, resp.text)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["title"], "Cozy Apartment")

    def test_get_all_places(self):
        """Test GET /api/v1/places/ returns list of places."""
        resp = requests.get(self.BASE_URL + "/")
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertIsInstance(resp.json(), list)

    def test_update_place(self):
        """Test PUT /api/v1/places/<place_id> updates place data."""
        # Create user
        user_payload = {
            "first_name": "PlaceOwner2",
            "last_name": "Tester2",
            "email": "owner2@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertEqual(user_resp.status_code, 201, user_resp.text)
        owner_id = user_resp.json()["id"]

        # Create place
        place_payload = {
            "title": "Old Title",
            "description": "Old desc",
            "price": 50,
            "latitude": 10.0,
            "longitude": 20.0,
            "owner_id": owner_id,
            "amenities": []
        }
        create_resp = requests.post(self.BASE_URL + "/", json=place_payload)
        self.assertEqual(create_resp.status_code, 201, create_resp.text)
        place_id = create_resp.json()["id"]

        # Update place
        update_payload = {"title": "New Title", "price": 200}
        update_url = f"{self.BASE_URL}/{place_id}"
        update_resp = requests.put(update_url, json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["title"], "New Title")
        self.assertEqual(updated_data["price"], 200)

    def test_get_single_place(self):
        """Test GET /api/v1/places/<place_id> retrieves a place by ID."""
        # Create user
        user_payload = {
            "first_name": "Owner3",
            "last_name": "Tester3",
            "email": "owner3@example.com"
        }
        user_resp = requests.post("http://127.0.0.1:5001/api/v1/users/", json=user_payload)
        self.assertEqual(user_resp.status_code, 201, user_resp.text)
        owner_id = user_resp.json()["id"]

        # Create place
        place_payload = {
            "title": "Another Place",
            "description": "Testing get place",
            "price": 99,
            "latitude": 1.1,
            "longitude": 2.2,
            "owner_id": owner_id,
            "amenities": []
        }
        create_resp = requests.post(self.BASE_URL + "/", json=place_payload)
        self.assertEqual(create_resp.status_code, 201, create_resp.text)
        place_id = create_resp.json()["id"]

        # Retrieve place
        get_url = f"{self.BASE_URL}/{place_id}"
        get_resp = requests.get(get_url)
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        data = get_resp.json()
        self.assertEqual(data["price"], 99)
        self.assertEqual(data["title"], "Another Place")

if __name__ == "__main__":
    unittest.main()
