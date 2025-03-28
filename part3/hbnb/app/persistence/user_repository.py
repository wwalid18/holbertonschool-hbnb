# app/persistence/user_repository.py
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app import db

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_by_email(self, email):
        """
        Retrieve a user by their email address.
        This wraps the generic get_by_attribute method for clarity and potential future extensions.
        """
        return self.get_by_attribute('email', email)

    def reset_password(self, email, new_password):
        """
        Reset the password for the user identified by email.
        The new password is hashed using the User model's hash_password method.
        """
        user = self.get_by_email(email)
        if not user:
            raise ValueError("User not found.")
        user.hash_password(new_password)
        db.session.commit()  # Commit the changes to the database
        return user
