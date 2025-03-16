import uuid
from datetime import datetime

class BaseModel:
    """A base class for all models to handle common attributes and methods."""

    _instances = {}  # Store instances in memory

    def __init__(self):
        self.id = str(uuid.uuid4())  # Store UUID as a string
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

        self._instances[self.id] = self  # Register instance

    def save(self):
        """Update the updated_at timestamp whenever the object is modified."""
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update attributes based on a dictionary of new values.
        Ensures that only existing attributes are updated.
        """
        for key, value in data.items():
            if hasattr(self, key):  # Only update existing attributes
                setattr(self, key, value)
            else:
                raise ValueError(f"Attribute '{key}' does not exist in {self.__class__.__name__}")
        self.save()

    @classmethod
    def get_by_id(cls, obj_id):
        """Retrieve an instance by its ID, return None if not found."""
        return cls._instances.get(obj_id)

    @classmethod
    def all_instances(cls):
        """Retrieve all instances of the class."""
        return list(cls._instances.values())

    @classmethod
    def delete(cls, obj_id):
        """Delete an instance by its ID, ensuring safe deletion."""
        if obj_id in cls._instances:
            del cls._instances[obj_id]
            return True
        return False  # Return False if object wasn't found

    def __repr__(self):
        return f"{self.__class__.__name__}(ID: {self.id}, Created: {self.created_at}, Updated: {self.updated_at})"
