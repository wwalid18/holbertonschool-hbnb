# app/models/place.py
from app.models.base_model import BaseModel
from app import db

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'
    
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key linking this place to its owner (User)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships:
    # A place can have many reviews
    reviews = db.relationship('Review', backref='place', lazy=True)
    # A place can have many amenities (many-to-many relationship)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            # Assuming the User model's to_dict() is available
            'owner': self.owner.to_dict() if self.owner else None,
            # Convert amenities to a list of dictionaries if they exist
            'amenities': [amenity.to_dict() for amenity in self.amenities]
        }
    
    def __repr__(self):
        return f"Place({self.title}, Price: {self.price})"
