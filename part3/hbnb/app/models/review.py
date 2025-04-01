# app/models/review.py
from app.models.base_model import BaseModel
from app import db

class Review(BaseModel):
    __tablename__ = 'Review'
    
    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('Place.id'), nullable=False)
    
    def __init__(self, text, rating, user, place):
        if not text or not isinstance(text, str):
            raise ValueError("Review text is required and must be a string.")
        if not isinstance(rating, int) or rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        if not user:
            raise ValueError("User must be provided.")
        if not place:
            raise ValueError("Place must be provided.")
        self.text = text.strip()
        self.rating = rating
        self.user = user   # User instance
        self.place = place # Place instance
    
    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id if self.user else None,
            'place_id': self.place.id if self.place else None
        }
    
    def __repr__(self):
        return f"Review(Rating: {self.rating}, Place: {self.place.title if self.place else 'N/A'}, User: {self.user.first_name if self.user else 'N/A'})"
