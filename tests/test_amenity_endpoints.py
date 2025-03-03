import unittest
import requests

class TestAmenityEndpoints(unittest.TestCase):
    BASE_URL = "http://127.0.0.1:5001/api/v1/amenities"

    def test_create_amenity(self):
        """Test POST /api/v1/amenities/ creates a new amenity."""
        amen_payload = {"name": "Wi-Fi"}
        resp = requests.post(self.BASE_URL + "/", json=amen_payload)
        self.assertIn(resp.status_code, [200,201], resp.text)  # might be 200 or 201
        data = resp.json()
        self.assertIn("id", data)
        self.assertEqual(data["name"], "Wi-Fi")

    def test_get_all_amenities(self):
        """Test GET /api/v1/amenities/ returns list of amenities."""
        resp = requests.get(self.BASE_URL + "/")
        self.assertEqual(resp.status_code, 200, resp.text)
        self.assertIsInstance(resp.json(), list)

    def test_update_amenity(self):
        """Test PUT /api/v1/amenities/<amenity_id> updates amenity data."""
        # Create amenity
        amen_payload = {"name": "Parking"}
        create_resp = requests.post(self.BASE_URL + "/", json=amen_payload)
        self.assertIn(create_resp.status_code, [200,201], create_resp.text)
        amen_id = create_resp.json()["id"]

        # Update amenity
        update_payload = {"name": "Valet Parking"}
        update_url = f"{self.BASE_URL}/{amen_id}"
        update_resp = requests.put(update_url, json=update_payload)
        self.assertEqual(update_resp.status_code, 200, update_resp.text)
        updated_data = update_resp.json()
        self.assertEqual(updated_data["name"], "Valet Parking")

    def test_get_single_amenity(self):
        """Test GET /api/v1/amenities/<amenity_id> retrieves an amenity by ID."""
        # Create amenity
        amen_payload = {"name": "Gym"}
        create_resp = requests.post(self.BASE_URL + "/", json=amen_payload)
        self.assertIn(create_resp.status_code, [200,201], create_resp.text)
        amen_id = create_resp.json()["id"]

        # Retrieve amenity
        get_url = f"{self.BASE_URL}/{amen_id}"
        get_resp = requests.get(get_url)
        self.assertEqual(get_resp.status_code, 200, get_resp.text)
        data = get_resp.json()
        self.assertEqual(data["name"], "Gym")

if __name__ == "__main__":
    unittest.main()
