import unittest
from app import create_app
from app.services.facade import HBnBFacade

class TestReviewEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and create necessary data."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

        # Create an admin user
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Admin",
            "last_name": "User",
            "email": "admin@example.com",
            "is_admin": True
        })
        self.admin_user_id = response.get_json()["id"]

        # Create a place
        response = self.client.post('/api/v1/places/', json={
            "title": "Nice Cabin",
            "price": 150,
            "latitude": 38.0,
            "longitude": -77.0,
            "owner_id": self.admin_user_id
        })
        self.place_id = response.get_json()["id"]

    ### CREATE REVIEW TESTS ###
    def test_create_review_success(self):
        """Test creating a review with valid data."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Great place!",
            "rating": 5,
            "user_id": self.admin_user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_review_invalid_rating(self):
        """Test creating a review with an invalid rating."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "Not great",
            "rating": 6,
            "user_id": self.admin_user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_missing_fields(self):
        """Test creating a review with missing fields."""
        response = self.client.post('/api/v1/reviews/', json={
            "text": "No rating provided",
            "user_id": self.admin_user_id,
            "place_id": self.place_id
        })
        self.assertEqual(response.status_code, 400)

    ### GET REVIEWS TESTS ###
    def test_get_all_reviews(self):
        """Test retrieving all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_reviews_by_place(self):
        """Test retrieving reviews for a specific place."""
        response = self.client.get(f'/api/v1/reviews?place_id={self.place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_review_not_found(self):
        """Test retrieving a review that does not exist."""
        response = self.client.get('/api/v1/reviews/99999')
        self.assertEqual(response.status_code, 404)

if __name__ == '__main__':
    unittest.main()
