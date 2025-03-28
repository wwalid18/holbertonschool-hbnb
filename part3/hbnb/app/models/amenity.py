# app/models/amenity.py
from app.models.base_model import BaseModel
from app import db

class Amenity(BaseModel):
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False)
    
    def __init__(self, name):
        if not name or not isinstance(name, str):
            raise ValueError("Amenity name is required and must be a string.")
        if len(name) > 50:
            raise ValueError("Amenity name must not exceed 50 characters.")
        self.name = name.strip()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name
        }
    
    def __repr__(self):
        return f"Amenity({self.name})"
