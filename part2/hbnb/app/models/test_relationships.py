from user import User
from place import Place
from review import Review
from amenity import Amenity

owner = User("Alice", "Smith", "alice@example.com")
print("User Created:", owner.id, owner.first_name, owner.email)

place1 = Place("Cozy Apartment", "A nice place to stay", 100, 37.7749, -122.4194, owner)
place2 = Place("Luxury Villa", "An ocean view paradise", 500, 48.8566, 2.3522, owner)

print("Place 1:", place1.id, place1.title, "owned by", place1.owner.first_name)
print("Place 2:", place2.id, place2.title, "owned by", place2.owner.first_name)

review1 = Review("Amazing stay!", 5, place1, owner)
review2 = Review("Could be better.", 3, place1, owner)

place1.add_review(review1)
place1.add_review(review2)

print("Reviews for Place 1:")
for review in place1.reviews:
    print("-", review.text, "by", review.user.first_name, "Rating:", review.rating)

wifi = Amenity("Wi-Fi")
parking = Amenity("Parking")

place1.add_amenity(wifi)
place1.add_amenity(parking)

print("Amenities for Place 1:")
for amenity in place1.amenities:
    print("-", amenity.name)
