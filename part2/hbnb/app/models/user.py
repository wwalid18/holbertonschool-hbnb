import re
from base_model import BaseModel

class User(BaseModel):
    """User class representing a system user"""

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        self.first_name = first_name[:50] if len(first_name) <= 50 else first_name[:50]
        self.last_name = last_name[:50] if len(last_name) <= 50 else last_name[:50]

        if self.validate_email(email):
            self.email = email
        else:
            raise ValueError("Invalid email format")

        self.is_admin = is_admin

    def validate_email(self, email):
        """Check if the email is in a valid format"""
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None
