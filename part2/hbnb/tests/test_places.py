import unittest
from unittest.mock import patch
from app import create_app
from flask import json

class TestPlaceEndpoints(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()  # Ensure your app is properly created
        cls.client = cls.app.test_client()

    @patch('app.services.facade.create_place')
    def test_create_place(self, mock_create_place):
        # Define mock return value
        mock_create_place.return_value = {
            'id': 'place_123',
            'title': 'Beautiful Beach House',
            'description': 'A house by the beach',
            'price': 200.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'user_123'
        }

        # Test data
        place_data = {
            'title': 'Beautiful Beach House',
            'description': 'A house by the beach',
            'price': 200.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'user_123'
        }

        response = self.client.post('/api/v1/places', data=json.dumps(place_data), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['title'], 'Beautiful Beach House')
        mock_create_place.assert_called_once_with(place_data)  # Verify the function was called

    @patch('app.services.facade.get_all_places')
    def test_get_places(self, mock_get_all_places):
        # Mock return value
        mock_get_all_places.return_value = [
            {'id': 'place_1', 'title': 'Beach House', 'price': 150.0},
            {'id': 'place_2', 'title': 'Mountain Cabin', 'price': 200.0}
        ]

        response = self.client.get('/api/v1/places')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json), 2)

    @patch('app.services.facade.get_place')
    def test_get_place_by_id(self, mock_get_place):
        mock_get_place.return_value = {'id': 'place_1', 'title': 'Beach House'}

        response = self.client.get('/api/v1/places/place_1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['id'], 'place_1')

    @patch('app.services.facade.get_place')
    def test_get_place_not_found(self, mock_get_place):
        mock_get_place.return_value = None

        response = self.client.get('/api/v1/places/nonexistent_place')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Place not found')

    @patch('app.services.facade.update_place')
    def test_update_place(self, mock_update_place):
        updated_data = {
            'title': 'Updated Beach House',
            'description': 'Newly renovated beach house',
            'price': 250.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'user_123'
        }

        mock_update_place.return_value = {
            'id': 'place_1',
            'title': 'Updated Beach House',
            'description': 'Newly renovated beach house',
            'price': 250.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'user_123'
        }

        response = self.client.put('/api/v1/places/place_1', data=json.dumps(updated_data), content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Updated Beach House')

if __name__ == '__main__':
    unittest.main()
