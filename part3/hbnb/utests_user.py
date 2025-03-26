import unittest
from app import create_app
from app.services.facade import HBnBFacade
from app.models.user import User

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and a clean facade."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    def test_create_user_success(self):
        """Test creating a user with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_user_duplicate_email(self):
        """Test trying to create a user with an email that already exists."""
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        self.client.post('/api/v1/users/', json=user_data)  # First user creation
        response = self.client.post('/api/v1/users/', json=user_data)  # Duplicate
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Email already registered')

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data (empty name and invalid email)."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_get_all_users(self):
        """Test retrieving a list of users."""
        # Create a user first
        self.client.post('/api/v1/users/', json={
            "first_name": "Alice",
            "last_name": "Smith",
            "email": "alice@example.com"
        })
        
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreaterEqual(len(data), 1)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        # Create a user first
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "bob@example.com"
        })
        user_id = response.get_json()["id"]
        
        # Fetch the user by ID
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving a user that does not exist."""
        response = self.client.get('/api/v1/users/99999')  # Non-existent ID
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()
import unittest
from app import create_app
from app.services.facade import HBnBFacade
from app.models.user import User

class TestUserEndpoints(unittest.TestCase):
    def setUp(self):
        """Set up the Flask test client and a clean facade."""
        self.app = create_app()
        self.client = self.app.test_client()
        self.facade = HBnBFacade()

    ### ✅ CREATE USER TESTS ###
    def test_create_user_success(self):
        """Test creating a user with valid data."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('id', data)

    def test_create_user_duplicate_email(self):
        """Test trying to create a user with an email that already exists."""
        user_data = {
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        }
        self.client.post('/api/v1/users/', json=user_data)  # First user creation
        response = self.client.post('/api/v1/users/', json=user_data)  # Duplicate
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertEqual(data['error'], 'Email already registered')

    def test_create_user_invalid_data(self):
        """Test creating a user with invalid data (empty name and invalid email)."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    ### ✅ GET USERS TESTS ###
    def test_get_all_users(self):
        """Test retrieving a list of users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)

    def test_get_user_by_id(self):
        """Test retrieving a user by ID."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Bob",
            "last_name": "Marley",
            "email": "bob@example.com"
        })
        user_id = response.get_json()["id"]
        
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['id'], user_id)

    def test_get_user_not_found(self):
        """Test retrieving a user that does not exist."""
        response = self.client.get('/api/v1/users/99999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error'], 'User not found')

    ### ✅ UPDATE USER TESTS (if supported) ###
    def test_update_user_success(self):
        """Test updating a user's information successfully."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Charlie",
            "last_name": "Brown",
            "email": "charlie@example.com"
        })
        user_id = response.get_json()["id"]
        
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Charles"
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], "Charles")

    def test_update_user_invalid_email(self):
        """Test updating a user with an invalid email."""
        response = self.client.put('/api/v1/users/1', json={
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)

    def test_update_user_not_found(self):
        """Test updating a user that does not exist."""
        response = self.client.put('/api/v1/users/99999', json={
            "first_name": "New Name"
        })
        self.assertEqual(response.status_code, 404)

    ### ✅ DELETE USER TESTS (if supported) ###
    def test_delete_user_success(self):
        """Test deleting an existing user."""
        response = self.client.post('/api/v1/users/', json={
            "first_name": "David",
            "last_name": "Smith",
            "email": "david@example.com"
        })
        user_id = response.get_json()["id"]
        
        response = self.client.delete(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)

    def test_delete_user_not_found(self):
        """Test deleting a non-existent user."""
        response = self.client.delete('/api/v1/users/99999')
        self.assertEqual(response.status_code, 404)
        data = response.get_json()
        self.assertEqual(data['error'], 'User not found')

if __name__ == '__main__':
    unittest.main()
