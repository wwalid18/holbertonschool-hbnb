# HBnB - Airbnb Clone API & Front-End

This project is an Airbnb clone called HBnB. It consists of a back-end API built using Flask and a front-end interface using HTML, CSS, and JavaScript. The application allows users to browse available places, view detailed information for each place (including amenities and reviews), and submit reviews when authenticated.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [API Endpoints](#api-endpoints)
- [Usage](#usage)
- [CORS Configuration](#cors-configuration)
- [License](#license)

## Overview

HBnB is an Airbnb clone that provides both a RESTful API and a dynamic client-side interface. The API is built using Flask and leverages Flask-Restx, SQLAlchemy, and JWT-based authentication. The front end interacts with the API using the Fetch API, updating the user interface dynamically without page reloads.

## Features

- **User Authentication:**  
  - Login via JWT authentication.
  - JWT token is stored in cookies.
  - Conditional display (or redirection) based on authentication status.

- **Place Listings:**  
  - Fetch and display a list of available places.
  - Client-side filtering by maximum price.
  - Each place card displays title, description, price, and location.
  - "View Details" button navigates to a detailed page for each place.

- **Place Details:**  
  - Display detailed information about a selected place, including amenities and reviews.
  - Extract the place ID from the URL query parameters.
  - Authenticated users can submit reviews via an AJAX request.

- **Review Submission:**  
  - Uses the Fetch API to submit reviews.
  - Includes JWT token in the Authorization header.
  - On success, displays a success message and clears the form; on failure, shows an error message.

## Technologies Used

- **Back-End:**  
  - Python with Flask, Flask-Restx, SQLAlchemy, Flask-JWT-Extended, Flask-Migrate
  - MySQL (using PyMySQL)
  - Flask-CORS for handling cross-origin requests

- **Front-End:**  
  - HTML5, CSS3, JavaScript (Fetch API)
  - Responsive design principles

## Project Structure

- /hbnb
- ├── app/
- │   ├── __init__.py              # Application factory, extension initialization, and route registration
- │   ├── models/
- │   │   ├── __init__.py          # Import all models (User, Place, Review, Amenity)
- │   │   ├── base_model.py        # Base model with common functionality
- │   │   ├── user.py              # User model, password hashing and verification
- │   │   ├── place.py             # Place model with relationships to Amenity and Review
- │   │   ├── review.py            # Review model
- │   │   └── amenity.py           # Amenity model
- │   ├── api/
- │   │   └── v1/
- │   │       ├── auth.py          # Authentication endpoints (login, reset password)
- │   │       ├── users.py         # Admin-only endpoints for managing users
- │   │       ├── places.py        # Endpoints for managing places
- │   │       ├── reviews.py       # Endpoints for managing reviews
- │   │       └── amenities.py     # Endpoints for managing amenities
- │   ├── persistence/
- │   │   ├── repository.py        # Abstract and SQLAlchemy repository implementations
- │   │   └── user_repository.py   # Custom repository for User-specific operations
- │   └── services/
- │       ├── __init__.py          # Exposes the HBnBFacade instance
- │       └── facade.py            # Facade pattern to centralize business logic
- ├── config.py                    # Application configuration settings (development, production)
- ├── run.py                       # Entry point to run the Flask application
- ├── part4/ (front-end files)
- │   ├── index.html               # Main page listing all places
- │   ├── login.html               # Login page
- │   ├── place.html               # Place details page
- │   ├── add_review.html          # (Optional) Separate page for adding reviews
- │   ├── styles.css               # CSS file for front-end styling
- │   ├── auth.js                  # JavaScript for authentication (login, logout)
- │   ├── index.js                 # JavaScript for fetching and filtering places
- │   ├── place.js                 # JavaScript for fetching place details and handling review submission
- │   └── add_review.js            # JavaScript for submitting reviews
- └── README.md                    # This file


## Setup and Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/wwalid18/holbertonschool-hbnb.git

 ### **Authors**
 This project is made by:
 - [![GitHub](https://img.shields.io/badge/GitHub-Nourkasmi-000000?style=flat&logo=github)](https://github.com/Nourkasmi)
 - [![GitHub](https://img.shields.io/badge/GitHub-wwalid18-000000?style=flat&logo=github)](https://github.com/wwalid18)