import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestPlaceEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and a clean facade."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

        # Create an admin user to own places
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "is_admin": True
        })
        self.admin_user_id = response.get_json()["id"]

    ### ✅ CREATE PLACE TESTS ###
    def test_create_place_success(self):
        """Test creating a place with valid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Cozy Apartment",
            "price": 100,
            "latitude": 37.7749,
            "longitude": -122.4194,
            "owner_id": self.admin_user_id
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_place_invalid_data(self):
        """Test creating a place with invalid data."""
        response = self.client.post('/api/v1/places/', json={
            "title": "",
            "price": -50,
            "latitude": 100,
            "longitude": 200,
            "owner_id": "1234"
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_non_admin(self):
        """Test that only admins can create places."""
        # Create a normal user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Regular",
            "last_name": "User",
            "email": "regular@example.com",
            "is_admin": False
        })
        user_id = response.get_json()["id"]

        response = self.client.post('/api/v1/places/', json={
            "title": "Unauthorized Place",
            "price": 200,
            "latitude": 35.0,
            "longitude": -80.0,
            "owner_id": user_id
        })
        self.assertEqual(response.status_code, 400)

    ### ✅ GET PLACE TESTS ###
    def test_get_all_places(self):
        """Test retrieving all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_place_by_id(self):
        """Test retrieving a place by ID."""
        response = self.client.post('/api/v1/places/', json={
            "title": "Beach House",
            "price": 300,
            "latitude": 25.0,
            "longitude": -75.0,
            "owner_id": self.admin_user_id
        })
        place_id = response.get_json()["id"]

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], place_id)

    def test_get_place_not_found(self):
        """Test retrieving a place that does not exist."""
        response = self.client.get('/api/v1/places/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
