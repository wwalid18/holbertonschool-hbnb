from app.models.base_model import BaseModel
from app import db, bcrypt

class User(BaseModel):
    __tablename__ = 'User'
    
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Relationships: A user can own many places and write many reviews.
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)
    
    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.email = email.strip()
        self.hash_password(password)
        self.is_admin = is_admin

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    
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
