# app/models/user.py
from app.models.base_model import BaseModel  # Import your BaseModel (updated for SQLAlchemy)
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'users'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationship: one-to-many with Place (assuming a Place model exists)
    places = db.relationship('Place', backref='owner', lazy=True)
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        """Hashes the password using bcrypt and stores the hashed password."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies the provided password against the stored hashed password."""
        return bcrypt.check_password_hash(self.password, password)
    
    def to_dict(self):
        """Converts the user instance to a dictionary (excluding the password)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        }
    
    def __repr__(self):
        return f"User({self.first_name} {self.last_name}, Email: {self.email})"
