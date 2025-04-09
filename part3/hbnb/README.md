<<<<<<< HEAD
# **HBnB Project**

## **Description**
HBnB is a RESTful API for an Airbnb-like application. It allows users to manage entities such as Users, Places, Reviews, and Amenities. The API uses JWT-based authentication and role-based access control to ensure secure operations. This project is part of the Holberton School curriculum.
=======
# **HBNB API - v1**

## **Description**
HBNB API is a RESTful API built using Flask and Flask-RESTx for the HBNB project. It provides endpoints to manage users, places, amenities, and reviews.

This project is part of the Holberton School curriculum.
>>>>>>> 5592a4f900611797c08927a08996b59175a6e040

---

## **Features**
<<<<<<< HEAD
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
=======
The HBNB API provides the following functionalities:

- **Users Management**
  - Create, retrieve, update, and delete users.

- **Places Management**
  - Create, retrieve, update, and delete places.
  - Associate places with amenities.
  - Retrieve reviews for places.

- **Amenities Management**
  - Create, retrieve, update, and delete amenities.

- **Reviews Management**
  - Create, retrieve, update, and delete reviews for places.
>>>>>>> 5592a4f900611797c08927a08996b59175a6e040

---

## **How It Works**
<<<<<<< HEAD
1. **Authentication:**
   - Users log in via the `/api/v1/auth/login` endpoint and receive a JWT token that contains their user ID and admin status.
2. **API Requests:**
   - API endpoints validate input data and enforce authentication/authorization using JWT and custom decorators.
3. **Business Logic & Data Access:**
   - The **HBnBFacade** (in `app/services/facade.py`) orchestrates operations and calls repository methods to interact with the MySQL database.
4. **Response Serialization:**
   - Model instances are converted to plain dictionaries using their `to_dict()` methods before being returned as JSON.
=======
1. The API is structured using Flask-RESTx.
2. Blueprints are used to organize endpoints (`/api/v1` prefix).
3. Each resource (Users, Places, Amenities, Reviews) has its own namespace.
4. A facade layer (`HBnBFacade`) handles business logic.
5. Uses models for request validation.
>>>>>>> 5592a4f900611797c08927a08996b59175a6e040

---

## **File Descriptions**

<<<<<<< HEAD
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
=======
### **app/api/v1/__init__.py**
- Initializes the API.
- Registers namespaces for users, places, amenities, and reviews.

### **app/api/v1/amenities.py**
- Endpoints for managing amenities:
  - `POST /api/v1/amenities/` - Create a new amenity.
  - `GET /api/v1/amenities/` - Retrieve all amenities.
  - `GET /api/v1/amenities/<amenity_id>` - Retrieve a specific amenity.
  - `PUT /api/v1/amenities/<amenity_id>` - Update an amenity.

### **app/api/v1/places.py**
- Endpoints for managing places:
  - `POST /api/v1/places/` - Create a new place.
  - `GET /api/v1/places/` - Retrieve all places.
  - `GET /api/v1/places/<place_id>` - Retrieve a specific place.
  - `PUT /api/v1/places/<place_id>` - Update a place.
  - `GET /api/v1/places/<place_id>/reviews` - Get all reviews for a place.

### **app/api/v1/reviews.py**
- Endpoints for managing reviews:
  - `POST /api/v1/reviews/` - Create a new review.
  - `GET /api/v1/reviews/` - Retrieve all reviews.
  - `GET /api/v1/reviews/<review_id>` - Retrieve a specific review.
  - `PUT /api/v1/reviews/<review_id>` - Update a review.

---

## **Requirements**
- **Operating System**: Linux, macOS or Windows
- **Programming Language**: Python3
- **Framework**: Flask, Flask-RESTx

---

## **Installation and Usage**
 - pip install -r requirements.txt
 - source /home/walid/holbertonschool-hbnb/part3/hbnb/hbnb_schema.sql;

 ---

### **Clone the repository**
```bash
git clone https://github.com/wwalid18/holbertonschool-hbnb.git
cd part2/Hbnb
python3 run.py

```
 --- 

### **Authors**
This project is made by:

- [![GitHub](https://img.shields.io/badge/GitHub-Nourkasmi-000000?style=flat&logo=github)](https://github.com/Nourkasmi)

- [![GitHub](https://img.shields.io/badge/GitHub-wwalid18-000000?style=flat&logo=github)](https://github.com/wwalid18)

 ### **Entity-Relationship Diagram**
<img src="db_diag.png" alt="follow this to understand relations between tables" width="500">
>>>>>>> 5592a4f900611797c08927a08996b59175a6e040
