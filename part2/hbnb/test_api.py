import requests

BASE_URL = "http://127.0.0.1:5000/api/v1"

def test_users():
    print("\n🔹 Testing User Creation...")
    response = requests.post(f"{BASE_URL}/users/", json={
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com"
    })
    print(response.status_code, response.json())

    user_id = response.json().get("id")
    if user_id:
        print("\n🔹 Testing Get User...")
        response = requests.get(f"{BASE_URL}/users/{user_id}")
        print(response.status_code, response.json())

        print("\n🔹 Testing Update User...")
        response = requests.put(f"{BASE_URL}/users/{user_id}", json={
            "first_name": "Jane"
        })
        print(response.status_code, response.json())

def test_amenities():
    print("\n🔹 Testing Amenity Creation...")
    response = requests.post(f"{BASE_URL}/amenities/", json={
        "name": "Wi-Fi"
    })
    print(response.status_code, response.json())

    amenity_id = response.json().get("id")
    if amenity_id:
        print("\n🔹 Testing Get Amenity...")
        response = requests.get(f"{BASE_URL}/amenities/{amenity_id}")
        print(response.status_code, response.json())

        print("\n🔹 Testing Update Amenity...")
        response = requests.put(f"{BASE_URL}/amenities/{amenity_id}", json={
            "name": "Swimming Pool"
        })
        print(response.status_code, response.json())

def test_places():
    print("\n🔹 Testing Place Creation...")
    # Creating a user first (to be the owner)
    user_response = requests.post(f"{BASE_URL}/users/", json={
        "first_name": "Alice",
        "last_name": "Smith",
        "email": "alice.smith@example.com"
    })
    user_id = user_response.json().get("id")

    # Creating an amenity first
    amenity_response = requests.post(f"{BASE_URL}/amenities/", json={
        "name": "Parking"
    })
    amenity_id = amenity_response.json().get("id")

    # Creating a place
    response = requests.post(f"{BASE_URL}/places/", json={
        "title": "Cozy Apartment",
        "description": "A comfortable place to stay",
        "price": 120.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id,
        "amenities": [amenity_id]
    })
    print(response.status_code, response.json())

    place_id = response.json().get("id")
    if place_id:
        print("\n🔹 Testing Get Place...")
        response = requests.get(f"{BASE_URL}/places/{place_id}")
        print(response.status_code, response.json())

        print("\n🔹 Testing Update Place...")
        response = requests.put(f"{BASE_URL}/places/{place_id}", json={
            "title": "Luxury Villa"
        })
        print(response.status_code, response.json())

def run_tests():
    test_users()
    test_amenities()
    test_places()

if __name__ == "__main__":
    run_tests()
