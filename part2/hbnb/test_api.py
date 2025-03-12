import requests
import time  # ✅ Ensure database updates before retrieving

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
    if not user_id:
        print("❌ User creation failed. Skipping further user tests.")
        return None

    time.sleep(1)  # ✅ Ensure database updates before retrieving

    print("\n🔹 Testing Get User...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(response.status_code, response.json())

    if response.status_code != 200:
        print(f"❌ Error: User {user_id} not found in retrieval!")
        return None

    return user_id  # ✅ Return user_id for further tests

def test_places():
    print("\n🔹 Testing Place Creation...")

    # ✅ Ensure user exists before creating place
    user_id = test_users()
    if not user_id:
        print("❌ No user created. Skipping place tests.")
        return

    # ✅ Ensure user retrieval works before continuing
    print(f"\n🔹 Verifying User Retrieval for ID {user_id}...")
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    print(response.status_code, response.json())

    if response.status_code != 200:
        print(f"❌ User {user_id} retrieval failed! Skipping place tests.")
        return

    # ✅ Ensure amenity exists before creating place
    response = requests.post(f"{BASE_URL}/amenities/", json={
        "name": "Wi-Fi"
    })
    print(response.status_code, response.json())

    amenity_id = response.json().get("id")
    if not amenity_id:
        print("❌ No amenity created. Skipping place tests.")
        return

    time.sleep(1)  # ✅ Ensure database updates before using data

    # ✅ Create a place
    print(f"\n🔹 Attempting to create place with owner {user_id} and amenity {amenity_id}...")
    response = requests.post(f"{BASE_URL}/places/", json={
        "title": "Cozy Apartment",
        "description": "A comfortable place to stay",
        "price": 120.0,
        "latitude": 37.7749,
        "longitude": -122.4194,
        "owner_id": user_id,  # ✅ Use correct owner_id
        "amenities": [amenity_id]
    })
    print(response.status_code, response.json())

    if response.status_code != 201:
        print("❌ Place creation failed. Skipping further place tests.")
        return

def run_tests():
    print("\n🚀 Running API Tests...\n")
    test_places()

if __name__ == "__main__":
    run_tests()
