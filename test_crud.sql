-- Test SELECT operations
SELECT * FROM users WHERE id = '36c9050e-ddd3-4c3b-9731-9f487208bbc1';
SELECT * FROM amenities;

-- Test INSERT operations
-- Insert a new user
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'John',
    'Doe',
    'john@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAXhZxQh6K6O',
    FALSE
);

-- Insert a new place
INSERT INTO places (id, title, description, price, latitude, longitude, owner_id)
VALUES (
    'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15',
    'Cozy Apartment',
    'A beautiful apartment in the city center',
    100.00,
    40.7128,
    -74.0060,
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14'
);

-- Link amenities to the place
INSERT INTO place_amenity (place_id, amenity_id)
VALUES 
    ('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11'),
    ('e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15', 'b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12');

-- Insert a review
INSERT INTO reviews (id, text, rating, user_id, place_id)
VALUES (
    'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16',
    'Great place to stay!',
    5,
    'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14',
    'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15'
);

-- Test SELECT operations after INSERT
SELECT * FROM places WHERE id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
SELECT a.name FROM amenities a
JOIN place_amenity pa ON a.id = pa.amenity_id
WHERE pa.place_id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
SELECT * FROM reviews WHERE place_id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';

-- Test UPDATE operations
UPDATE places 
SET price = 120.00, description = 'A beautiful apartment in the city center with great amenities'
WHERE id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';

UPDATE reviews 
SET rating = 4, text = 'Very good place to stay!'
WHERE id = 'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16';

-- Test SELECT operations after UPDATE
SELECT * FROM places WHERE id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
SELECT * FROM reviews WHERE id = 'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16';

-- Test DELETE operations (in correct order)
DELETE FROM reviews WHERE id = 'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16';
DELETE FROM place_amenity WHERE place_id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
DELETE FROM places WHERE id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
DELETE FROM users WHERE id = 'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14';

-- Verify deletions
SELECT * FROM users WHERE id = 'd0eebc99-9c0b-4ef8-bb6d-6bb9bd380a14';
SELECT * FROM places WHERE id = 'e0eebc99-9c0b-4ef8-bb6d-6bb9bd380a15';
SELECT * FROM reviews WHERE id = 'f0eebc99-9c0b-4ef8-bb6d-6bb9bd380a16'; 