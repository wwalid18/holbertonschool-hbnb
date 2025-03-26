import re
from app.models.base_model import BaseModel

class User(BaseModel):
    """A simple User class with basic attributes and relationships."""

    _users = {}  # Dictionary to store users and ensure unique emails

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()  # Call the BaseModel constructor (sets id, timestamps)

        # Validate first name and last name
        if not first_name or len(first_name) > 50:
            raise ValueError("First name is required (max 50 characters).")
        if not last_name or len(last_name) > 50:
            raise ValueError("Last name is required (max 50 characters).")

        # Validate email format
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, email):
            raise ValueError("Invalid email format.")

        # Ensure the email is unique
        if email in self._users:
            raise ValueError("Email already registered.")

        # Assign values
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.is_admin = is_admin
        self.places = []  # List to store places owned by this user

        # Store the user by email to ensure uniqueness
        self._users[email] = self  

    def add_place(self, place):
        """Link a place to this user."""
        from app.models.place import Place  # Avoid circular import
        if isinstance(place, Place) and place.owner == self:
            self.places.append(place)
        else:
            raise ValueError("Invalid place or owner mismatch.")

    def to_dict(self):
        """Convert the User object to a dictionary."""
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin  # Include is_admin in the dictionary
        }

    def __repr__(self):
        """Returns a readable string representation of the user."""
        return f"User({self.first_name} {self.last_name}, Email: {self.email}, Admin: {self.is_admin})"