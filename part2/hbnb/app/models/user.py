import re
from datetime import datetime

class User(BaseModel):
    """Represents a user with attributes and constraints."""
    
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = self.validate_name(first_name, "First name")
        self.last_name = self.validate_name(last_name, "Last name")
        self.email = self.validate_email(email)
        self.is_admin = is_admin
        self.places = []

    @staticmethod
    def validate_name(name, field):
        """Validate name fields (first_name, last_name)"""
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"{field} is required and must be a non-empty string.")
        if len(name) > 50:
            raise ValueError(f"{field} must not exceed 50 characters.")
        return name.strip()

    @staticmethod
    def validate_email(email):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not isinstance(email, str) or not re.match(email_regex, email):
            raise ValueError("Invalid email format.")
        return email.strip()

    def update(self, data):
        """Update user attributes with validation"""
        if 'first_name' in data:
            self.first_name = self.validate_name(data['first_name'], "First name")
        if 'last_name' in data:
            self.last_name = self.validate_name(data['last_name'], "Last name")
        if 'email' in data:
            self.email = self.validate_email(data['email'])
        if 'is_admin' in data:
            if not isinstance(data['is_admin'], bool):
                raise ValueError("is_admin must be a boolean value.")
            self.is_admin = data['is_admin']
        super().update(data)

    def add_place(self, place):
        """Associate a Place instance with this user"""
        if isinstance(place, Place) and place.owner == self:
            self.places.append(place)
        else:
            raise ValueError("Invalid place or owner mismatch.")

    def __repr__(self):
        return f"User({self.first_name} {self.last_name}, Email: {self.email}, Admin: {self.is_admin})"
