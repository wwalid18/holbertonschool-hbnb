-- Create the database
CREATE DATABASE IF NOT EXISTS hbnb;
USE hbnb;

-- Create the User table
CREATE TABLE IF NOT EXISTS User (
    id CHAR(36) PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the Place table
CREATE TABLE IF NOT EXISTS Place (
    id CHAR(36) PRIMARY KEY,  -- Use CHAR(36) for UUIDs
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    latitude FLOAT,
    longitude FLOAT,
    owner_id CHAR(36) NOT NULL,  -- Use CHAR(36) for UUIDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES User(id) ON DELETE CASCADE
);

-- Create the Review table
CREATE TABLE IF NOT EXISTS Review (
    id CHAR(36) PRIMARY KEY,  -- Use CHAR(36) for UUIDs
    text TEXT NOT NULL,
    rating INT,
    user_id CHAR(36) NOT NULL,  -- Use CHAR(36) for UUIDs
    place_id CHAR(36) NOT NULL,  -- Use CHAR(36) for UUIDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE (user_id, place_id),
    FOREIGN KEY (user_id) REFERENCES User(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE
);

-- Create the Amenity table
CREATE TABLE IF NOT EXISTS Amenity (
    id CHAR(36) PRIMARY KEY,  -- Use CHAR(36) for UUIDs
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the Place_Amenity table (Many-to-Many relationship)
CREATE TABLE IF NOT EXISTS Place_Amenity (
    place_id CHAR(36) NOT NULL,  -- Use CHAR(36) for UUIDs
    amenity_id CHAR(36) NOT NULL,  -- Use CHAR(36) for UUIDs
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES Place(id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenity(id) ON DELETE CASCADE
);

-- Insert initial data
-- Replace with your application-generated UUIDs for testing

INSERT INTO User (id, first_name, last_name, email, password, is_admin) VALUES
    (UUID(), 'Admin', 'HBnB', 'admin@hbnb.io', '$2b$12$eImG92jzjS76rYF6jFfYXO1x1Skx78Jep6jtp/f.WZHXO1Sz9YdO2', TRUE),
    (UUID(), 'John', 'Doe', 'john.doe@example.com', '$2b$12$7sImr.//j/2D/3yRmzAp8OeTOZnPZATJv7XymP7zN5j6ZekrJUXTG', FALSE),
    (UUID(), 'Jane', 'Doe', 'jane.doe@example.com', '$2b$12$5bKJp95kYOwFr.O1CvF/BO7WjFX5M78g.FXjUdPBb6UlOV9dOi8Ym', FALSE);

INSERT INTO Place (id, title, description, price, latitude, longitude, owner_id) VALUES
    (UUID(), 'Cozy Apartment', 'A nice cozy apartment in the city center.', 100.00, 40.7128, -74.0060, (SELECT id FROM User WHERE email = 'john.doe@example.com')),
    (UUID(), 'Beach House', 'A beautiful house near the beach.', 200.00, 34.0522, -118.2437, (SELECT id FROM User WHERE email = 'jane.doe@example.com'));

INSERT INTO Review (id, text, rating, user_id, place_id) VALUES
    (UUID(), 'Great place!', 5, (SELECT id FROM User WHERE email = 'john.doe@example.com'), (SELECT id FROM Place WHERE title = 'Cozy Apartment')),
    (UUID(), 'Had an amazing stay.', 4, (SELECT id FROM User WHERE email = 'jane.doe@example.com'), (SELECT id FROM Place WHERE title = 'Beach House'));

INSERT INTO Amenity (id, name) VALUES
    (UUID(), 'WiFi'),
    (UUID(), 'Swimming Pool'),
    (UUID(), 'Air Conditioning');

INSERT INTO Place_Amenity (place_id, amenity_id) VALUES
    ((SELECT id FROM Place WHERE title = 'Cozy Apartment'), (SELECT id FROM Amenity WHERE name = 'WiFi')),
    ((SELECT id FROM Place WHERE title = 'Cozy Apartment'), (SELECT id FROM Amenity WHERE name = 'Air Conditioning')),
    ((SELECT id FROM Place WHERE title = 'Beach House'), (SELECT id FROM Amenity WHERE name = 'Swimming Pool')),
    ((SELECT id FROM Place WHERE title = 'Beach House'), (SELECT id FROM Amenity WHERE name = 'Air Conditioning'));
