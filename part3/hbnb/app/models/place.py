from app.models.base_model import BaseModel
from app import db

# Association table for the many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('Place.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('Amenity.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'Place'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)
    
    # Relationships:
    # One-to-many with Review; Place will have many reviews.
    Review = db.relationship('Review', backref='place', lazy=True)
    # Many-to-many with Amenity via the association table.
    Amenity = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))
    
    def __init__(self, title, description, price, latitude, longitude, owner):
        if not title or len(title) > 100:
            raise ValueError("Title is required (max 100 characters).")
        if not description:
            raise ValueError("Description is required.")
        if not isinstance(price, (int, float)) or price <= 0:
            raise ValueError("Price must be a positive number.")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude must be between -90.0 and 90.0.")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude must be between -180.0 and 180.0.")
        if not owner:
            raise ValueError("Owner must be provided.")
        self.title = title.strip()
        self.description = description.strip()
        self.price = float(price)
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # The owner is a User instance.
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        }
    
    def __repr__(self):
        return f"Place({self.title}, Price: {self.price})"
