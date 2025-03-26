import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_restx import Api
from app.api.v1.amenities import api as amenities_ns
from app.services.facade import HBnBFacade

class TestAmenities(unittest.TestCase):
    def setUp(self):
        """Set up the test client and mock the facade."""
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.api.add_namespace(amenities_ns)
        self.client = self.app.test_client()

        # Mock the HBnBFacade methods
        self.facade_patcher = patch('app.api.v1.amenities.facade')
        self.mock_facade = self.facade_patcher.start()
        self.mock_facade_instance = MagicMock(spec=HBnBFacade)
        self.mock_facade.return_value = self.mock_facade_instance

    def tearDown(self):
        """Stop the patcher after each test."""
        self.facade_patcher.stop()

    def test_create_amenity_success(self):
        """Test creating a new amenity successfully."""
        # Mock the facade methods
        self.mock_facade_instance.get_amenity_by_name.return_value = None
        self.mock_facade_instance.create_amenity.return_value = MagicMock(id='123', name='WiFi')

        # Test data
        data = {
            'name': 'WiFi'
        }

        # Make the POST request
        response = self.client.post('/api/v1/amenities', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {
            'id': '123',
            'name': 'WiFi'
        })

    def test_create_amenity_duplicate(self):
        """Test creating a duplicate amenity."""
        # Mock the facade methods
        self.mock_facade_instance.get_amenity_by_name.return_value = MagicMock(id='123', name='WiFi')

        # Test data
        data = {
            'name': 'WiFi'
        }

        # Make the POST request
        response = self.client.post('/api/v1/amenities', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {
            'error': 'Amenity already exists'
        })

    def test_get_all_amenities(self):
        """Test retrieving all amenities."""
        # Mock the facade methods
        self.mock_facade_instance.get_all_amenities.return_value = [
            MagicMock(id='123', name='WiFi'),
            MagicMock(id='456', name='Pool')
        ]

        # Make the GET request
        response = self.client.get('/api/v1/amenities')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, [
            {'id': '123', 'name': 'WiFi'},
            {'id': '456', 'name': 'Pool'}
        ])

    def test_get_amenity_by_id_success(self):
        """Test retrieving an amenity by ID successfully."""
        # Mock the facade methods
        self.mock_facade_instance.get_amenity.return_value = MagicMock(id='123', name='WiFi')

        # Make the GET request
        response = self.client.get('/api/v1/amenities/123')

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'id': '123',
            'name': 'WiFi'
        })

    def test_get_amenity_by_id_not_found(self):
        """Test retrieving a non-existent amenity by ID."""
        # Mock the facade methods
        self.mock_facade_instance.get_amenity.return_value = None

        # Make the GET request
        response = self.client.get('/api/v1/amenities/999')

        # Assert the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            'error': 'Amenity not found'
        })

    def test_update_amenity_success(self):
        """Test updating an amenity successfully."""
        # Mock the facade methods
        self.mock_facade_instance.update_amenity.return_value = MagicMock(id='123', name='Free WiFi')

        # Test data
        data = {
            'name': 'Free WiFi'
        }

        # Make the PUT request
        response = self.client.put('/api/v1/amenities/123', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {
            'id': '123',
            'name': 'Free WiFi'
        })

    def test_update_amenity_not_found(self):
        """Test updating a non-existent amenity."""
        # Mock the facade methods
        self.mock_facade_instance.update_amenity.return_value = None

        # Test data
        data = {
            'name': 'Free WiFi'
        }

        # Make the PUT request
        response = self.client.put('/api/v1/amenities/999', json=data)

        # Assert the response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json, {
            'error': 'Amenity not found'
        })

if __name__ == '__main__':
    unittest.main()
