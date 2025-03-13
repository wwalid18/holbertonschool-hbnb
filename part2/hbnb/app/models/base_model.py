import uuid
from datetime import datetime

class BaseModel:
    """A base class for all models to handle common attributes and methods"""
    
    _instances = {}

    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        
        self._instances[self.id] = self

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes based on a dictionary of new values"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    @classmethod
    def get_by_id(cls, obj_id):
        """Retrieve an instance by its ID"""
        return cls._instances.get(obj_id, None)

    @classmethod
    def all_instances(cls):
        """Retrieve all instances of the class"""
        return list(cls._instances.values())

    def __repr__(self):
        return f"{self.__class__.__name__}(ID: {self.id}, Created: {self.created_at}, Updated: {self.updated_at})"
