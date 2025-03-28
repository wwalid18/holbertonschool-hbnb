import uuid
from datetime import datetime
from app import db  # db is the SQLAlchemy instance from app/__init__.py

class BaseModel(db.Model):
    __abstract__ = True  # This model is abstract; no table is created for it
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist in {self.__class__.__name__}")
        self.save()

    @classmethod
    def get_by_id(cls, obj_id):
        return cls.query.get(obj_id)

    @classmethod
    def all_instances(cls):
        return cls.query.all()

    @classmethod
    def delete(cls, obj_id):
        obj = cls.get_by_id(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}(ID: {self.id}, Created: {self.created_at}, Updated: {self.updated_at})"
