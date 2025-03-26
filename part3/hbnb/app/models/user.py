# app/models/user.py
import re
from app.models.db_base import DBBaseModel
from app import db, bcrypt

class User(DBBaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # Stores the hashed password
    is_admin = db.Column(db.Boolean, default=False)
    
    # One-to-many relationship with Place
    places = db.relationship('Place', backref='owner', lazy=True)
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.hash_password(password)  # Hash and store the password
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def add_place(self, place):
        """Link a place to this user.
        
        This method ensures that the provided place is a valid Place instance 
        and that the place's owner is this user. If the check passes, it adds 
        the place to the user's places collection.
        """
        from app.models.place import Place  # Avoid circular import
        if isinstance(place, Place) and place.owner == self:
            self.places.append(place)
        else:
            raise ValueError("Invalid place or owner mismatch.")
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
    
    def __repr__(self):
        return f"User({self.first_name} {self.last_name}, Email: {self.email})"

