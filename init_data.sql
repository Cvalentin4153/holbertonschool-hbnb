-- Insert admin user
-- Note: The password hash is for 'admin1234' using bcrypt
INSERT INTO users (id, first_name, last_name, email, password, is_admin)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewKyDAXhZxQh6K6O',
    TRUE
);

-- Insert initial amenities
INSERT INTO amenities (id, name) VALUES
    ('a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11', 'WiFi'),
    ('b0eebc99-9c0b-4ef8-bb6d-6bb9bd380a12', 'Swimming Pool'),
    ('c0eebc99-9c0b-4ef8-bb6d-6bb9bd380a13', 'Air Conditioning'); 