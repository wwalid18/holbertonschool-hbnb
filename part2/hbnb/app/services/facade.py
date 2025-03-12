from app.models import Place, User, Amenity
from app.persistence.repository import YourRepositoryClass


class HBnBFacade:
    def __init__(self):
        self.place_repo = PlaceRepository()

    def create_place(self, place_data):
        # Validate price, latitude, and longitude
        if place_data['price'] < 0:
            raise ValueError("Price cannot be negative.")
        if not (-90 <= place_data['latitude'] <= 90):
            raise ValueError("Latitude must be between -90 and 90.")
        if not (-180 <= place_data['longitude'] <= 180):
            raise ValueError("Longitude must be between -180 and 180.")
        
        # Create the Place
        place = Place(**place_data)
        
        # Save the place to the repository
        self.place_repo.save(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found.")
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        return places

    def update_place(self, place_id, place_data):
        # Fetch the place to be updated
        place = self.place_repo.get_by_id(place_id)
        if not place:
            raise ValueError("Place not found.")
        
        # Update the place attributes
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            if place_data['price'] < 0:
                raise ValueError("Price cannot be negative.")
            place.price = place_data['price']
        if 'latitude' in place_data:
            if not (-90 <= place_data['latitude'] <= 90):
                raise ValueError("Latitude must be between -90 and 90.")
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            if not (-180 <= place_data['longitude'] <= 180):
                raise ValueError("Longitude must be between -180 and 180.")
            place.longitude = place_data['longitude']
        
        # Save the updated place
        self.place_repo.save(place)
        return place
