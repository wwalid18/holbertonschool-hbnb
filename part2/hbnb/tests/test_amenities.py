import unittest
from app import create_app  # Import your app creation function
from app.services.facade import HBnBFacade
from flask_restx import Api

class TestAmenityEndpoints(unittest.TestCase):
    # Set up the test client
    def setUp(self):
        app = create_app()  # Create the app instance for testing
        self.app = app.test_client()  # Use Flask's test client
        self.app.testing = True  # Enable testing mode

        self.facade = HBnBFacade()  # Assuming facade is used for the business logic

    # Test POST /api/v1/amenities (Create Amenity)
    def test_create_amenity(self):
        data = {
            "name": "Swimming Pool"
        }
        response = self.app.post('/api/v1/amenities', json=data)  # Make POST request
        self.assertEqual(response.status_code, 201)  # Assert success status code
        self.assertIn('id', response.json)  # Ensure response contains 'id'
        self.assertEqual(response.json['name'], 'Swimming Pool')  # Assert the amenity name

    # Test GET /api/v1/amenities (List Amenities)
    def test_get_amenities(self):
        response = self.app.get('/api/v1/amenities')  # Make GET request
        self.assertEqual(response.status_code, 200)  # Assert success status code
        self.assertIsInstance(response.json, list)  # Ensure the response is a list

    # Test GET /api/v1/amenities/<amenity_id> (Get Amenity by ID)
    def test_get_amenity_by_id(self):
        amenity = self.facade.create_amenity({'name': 'Gym'})  # Create a test amenity
        response = self.app.get(f'/api/v1/amenities/{amenity.id}')  # Make GET request with the created amenity ID
        self.assertEqual(response.status_code, 200)  # Assert success status code
        self.assertEqual(response.json['name'], 'Gym')  # Assert the amenity name matches

    # Test PUT /api/v1/amenities/<amenity_id> (Update Amenity)
    def test_update_amenity(self):
        amenity = self.facade.create_amenity({'name': 'Sauna'})  # Create a test amenity
        data = {"name": "Updated Sauna"}
        response = self.app.put(f'/api/v1/amenities/{amenity.id}', json=data)  # Make PUT request
        self.assertEqual(response.status_code, 200)  # Assert success status code
        self.assertEqual(response.json['name'], 'Updated Sauna')  # Assert the amenity name was updated

    # Test PUT /api/v1/amenities/<amenity_id> (Amenity Not Found)
    def test_update_amenity_not_found(self):
        data = {"name": "Non-Existent Amenity"}
        response = self.app.put('/api/v1/amenities/nonexistent-id', json=data)  # Make PUT request with invalid ID
        self.assertEqual(response.status_code, 404)  # Assert not found status code
        self.assertEqual(response.json['error'], 'Amenity not found')  # Assert error message

if __name__ == '__main__':
    unittest.main()
