# app/models/review.py
from app.models.base_model import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'reviews'
    
    # Columns
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationships
    # (Assuming the User and Place models define backrefs, these relationships are optional)
    user = db.relationship('User', backref=db.backref('reviews', lazy=True))
    place = db.relationship('Place', backref=db.backref('reviews', lazy=True))
    
    def __init__(self, text, rating, user, place):
        super().__init__()
        
        # Validate review text
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string.")
        
        # Validate rating (must be an integer between 1 and 5)
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        
        # Validate that user and place are provided.
        if not user:
            raise ValueError("User must be provided.")
        if not place:
            raise ValueError("Place must be provided.")
        
        # Assign values
        self.text = text.strip()
        self.rating = rating
        self.user = user
        self.place = place

    def to_dict(self):
        """Convert the Review object to a dictionary."""
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user.id if self.user else None,
            "place_id": self.place.id if self.place else None
        }

    def __repr__(self):
        owner_info = self.place.title if self.place else "N/A"
        user_info = self.user.first_name if self.user else "N/A"
        return f"Review(Rating: {self.rating}, Place: {owner_info}, User: {user_info})"
