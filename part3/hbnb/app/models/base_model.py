# app/models/base_model.py
import uuid
from datetime import datetime
from app import db  # 'db' is the SQLAlchemy instance created in your app/__init__.py

class BaseModel(db.Model):
    __abstract__ = True  # This tells SQLAlchemy not to create a table for this model directly
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def save(self):
        """Add the instance to the database session and commit."""
        db.session.add(self)
        db.session.commit()
    
    def update(self, data):
        """
        Update attributes based on a dictionary of new values.
        Ensures that only existing attributes are updated, then commits the changes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist in {self.__class__.__name__}")
        self.save()
    
    @classmethod
    def get_by_id(cls, obj_id):
        """Retrieve an instance by its ID using a SQLAlchemy query."""
        return cls.query.get(obj_id)
    
    @classmethod
    def all_instances(cls):
        """Retrieve all instances using a SQLAlchemy query."""
        return cls.query.all()
    
    @classmethod
    def delete(cls, obj_id):
        """Delete an instance by its ID and commit the deletion."""
        obj = cls.get_by_id(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False
    
    def __repr__(self):
        return f"{self.__class__.__name__}(ID: {self.id}, Created: {self.created_at}, Updated: {self.updated_at})"
