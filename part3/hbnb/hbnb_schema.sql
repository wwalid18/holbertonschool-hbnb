-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb;
USE hbnb;

-- Create the User table
CREATE TABLE IF NOT EXISTS User (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Create the Place table
CREATE TABLE IF NOT EXISTS Place (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id INT NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Create the Review table
CREATE TABLE IF NOT EXISTS Review (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE
);

-- Create the Amenity table
CREATE TABLE IF NOT EXISTS Amenity (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Create the Place_Amenity table (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Insert initial data
INSERT INTO User (id, first_name, last_name, email, password, is_admin) VALUES
    (1, 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$eImG92jzjS76rYF6jFfYXO1x1Skx78Jep6jtp/f.WZHXO1Sz9YdO2', TRUE),
    (2, 'John', 'Doe', 'john.doe@example.com', '$2b$12$7sImr.//j/2D/3yRmzAp8OeTOZnPZATJv7XymP7zN5j6ZekrJUXTG', FALSE),
    (3, 'Jane', 'Doe', 'jane.doe@example.com', '$2b$12$5bKJp95kYOwFr.O1CvF/BO7WjFX5M78g.FXjUdPBb6UlOV9dOi8Ym', FALSE);

INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id) VALUES
    (1, 'Cozy Apartment', 'A nice cozy apartment in the city center.', 100.00, 40.7128, -74.0060, 2),
    (2, 'Beach House', 'A beautiful house near the beach.', 200.00, 34.0522, -118.2437, 3);

INSERT INTO Review (id, text, rating, user_id, place_id) VALUES
    (1, 'Great place!', 5, 2, 1),
    (2, 'Had an amazing stay.', 4, 3, 2);

INSERT INTO Amenity (id, name) VALUES
    (1, 'WiFi'),
    (2, 'Swimming Pool'),
    (3, 'Air Conditioning');

INSERT INTO Place_Amenity (place_id, amenity_id) VALUES
    (1, 1),
    (1, 3),
    (2, 2),
    (2, 3);
