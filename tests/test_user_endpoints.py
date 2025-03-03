import unittest
import requests

class TestUserEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001/api/v1/users"

    def test_create_user(self):
        """Test POST /api/v1/users creates a user."""
        payload = {
            "first_name": "Testy",
            "last_name": "McTestFace",
            "email": "testy@example.com"
        }
        resp = requests.post(self.BASE_URL + "/", json=payload)
        self.assertEqual(resp.status_code, 201, resp.text)
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["first_name"], "Testy")

    def test_get_all_users(self):
        """Test GET /api/v1/users returns list of users."""
        resp = requests.get(self.BASE_URL + "/")
        self.assertEqual(resp.status_code, 200)
        self.assertIsInstance(resp.json(), list)

    def test_update_user(self):
        """Test PUT /api/v1/users/<user_id> updates user data."""
        # First, create a user
        create_payload = {
            "first_name": "ToBeUpdated",
            "last_name": "BeforeUpdate",
            "email": "before@example.com"
        }
        create_resp = requests.post(self.BASE_URL + "/", json=create_payload)
        user_id = create_resp.json()["id"]

        # Now, update that user
        update_payload = {
            "first_name": "AfterUpdate"
        }
        update_url = f"{self.BASE_URL}/{user_id}"
        update_resp = requests.put(update_url, json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["first_name"], "AfterUpdate")

    # ... Additional tests for GET /users/<user_id>, etc.

if __name__ == "__main__":
    unittest.main()
