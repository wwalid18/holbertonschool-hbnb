# **HBnB Project**

## **Description**
HBnB is a RESTful API for an Airbnb-like application. It allows users to manage entities such as Users, Places, Reviews, and Amenities. The API uses JWT-based authentication and role-based access control to ensure secure operations. This project is part of the Holberton School curriculum.

---

## **Features**
The HBnB API supports the following functionalities:

- **User Management:**
  - **Create, Update, Retrieve, and Delete Users:**  
    Administrators can manage any user account.
  - **Password Hashing:**  
    User passwords are securely hashed before being stored.
  - **Unique Email Constraint:**  
    Ensures no duplicate emails are allowed.

- **Place Management:**
  - **CRUD Operations for Places:**  
    Users can create, update, retrieve, and delete places.
  - **Ownership Association:**  
    Each place is linked to a user (owner).
  - **Admin Override:**  
    Administrators can bypass ownership restrictions for updating/deleting.

- **Review Management:**
  - **CRUD Operations for Reviews:**  
    Users can create, update, retrieve, and delete reviews.
  - **Relationship Enforcement:**  
    Reviews link a user and a place; users can only review places they do not own, and only once per place.

- **Amenity Management:**
  - **Admin-Only Operations:**  
    Administrators can create, update, and delete amenities.
  - **Many-to-Many Association:**  
    Amenities are associated with places via a join table (`Place_Amenity`).

- **Authentication & Authorization:**
  - **JWT-Based Security:**  
    Endpoints are protected by JWT authentication.
  - **Role-Based Access Control:**  
    Custom decorators enforce that only authorized users (or admins) can perform restricted actions.

- **Database Persistence:**
  - **MySQL Database:**  
    Data is persisted using MySQL with SQLAlchemy ORM.
  - **Migrations:**  
    Database schema changes are managed with Alembic/Flask-Migrate.

- **ER Diagram:**
  - Mermaid.js diagrams visually represent the database schema and relationships.

---

## **How It Works**
1. **Authentication:**
   - Users log in via the `/api/v1/auth/login` endpoint and receive a JWT token that contains their user ID and admin status.
2. **API Requests:**
   - API endpoints validate input data and enforce authentication/authorization using JWT and custom decorators.
3. **Business Logic & Data Access:**
   - The **HBnBFacade** (in `app/services/facade.py`) orchestrates operations and calls repository methods to interact with the MySQL database.
4. **Response Serialization:**
   - Model instances are converted to plain dictionaries using their `to_dict()` methods before being returned as JSON.

---

## **File Descriptions**

### **app/__init__.py**
- **Role:** Application factory that creates and configures the Flask app, initializes extensions (SQLAlchemy, JWT, Bcrypt, Migrate), and registers API namespaces.

### **app/config.py**
- **Role:** Contains configuration settings such as `SECRET_KEY` and `SQLALCHEMY_DATABASE_URI` for MySQL.

### **app/models/**
- **Role:** Contains SQLAlchemy models mapping entities to database tables.
  - **base_model.py:**  
    Defines the BaseModel with common fields (`id`, `created_at`, `updated_at`) and helper methods.
  - **user.py:**  
    Maps the User entity (`first_name`, `last_name`, `email`, `password`, `is_admin`).
  - **place.py:**  
    Maps the Place entity (`title`, `description`, `price`, `latitude`, `longitude`, `owner_id`) and defines relationships with Review and Amenity.
  - **review.py:**  
    Maps the Review entity (`text`, `rating`, `user_id`, `place_id`).
  - **amenity.py:**  
    Maps the Amenity entity (`name`).

### **app/services/facade.py**
- **Role:** Provides business logic methods (e.g., `create_user()`, `create_place()`, `create_review()`, `create_amenity()`) and interacts with the repository layer.

### **app/persistence/**
- **Role:** Implements the repository pattern for data access.
  - **repository.py:**  
    Contains the generic SQLAlchemyRepository for CRUD operations.
  - **user_repository.py:**  
    A dedicated repository for user-specific queries (e.g., `get_by_email`, `reset_password`).

### **app/api/v1/**
- **Role:** Contains the RESTful API endpoints.
  - **auth.py:** Authentication endpoints (login, password reset).
  - **users.py:** User management endpoints.
  - **places.py:** Place management endpoints.
  - **reviews.py:** Review management endpoints.
  - **amenities.py:** Amenity management endpoints (admin-only).

### **app/utils/decorators.py**
- **Role:** Contains custom decorators (e.g., `admin_required`) to enforce role-based access control.

### **migrations/**
- **Role:** Contains Alembic migration scripts for evolving the database schema.

### **run.py**
- **Role:** The entry point to run the Flask application.

---

## **Compilation/Installation**
To set up the HBnB project, follow these steps:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/wwalid18/holbertonschool-hbnb.git
   cd holbertonschool-hbnb/part3/hbnb
