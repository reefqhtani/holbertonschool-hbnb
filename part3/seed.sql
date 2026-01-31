-- Insert an Admin User
-- ID: 36c9050e-577e-40d2-b4c6-2d9385002012
-- Password: 'password123' (hashed)
INSERT INTO users (id, email, password, first_name, last_name, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-577e-40d2-b4c6-2d9385002012',
    'admin@hbnb.io',
    '$2b$12$MQ0.F/V.Wd4n7Lz0.XwO.u.A6d6t6r6v6s6w6x6y6z6A6B6C6D6E', 
    'Admin',
    'HBnB',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Amenities
-- ID: 1
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ID: 2
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440001',
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- ID: 3
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    '550e8400-e29b-41d4-a716-446655440002',
    'Air Conditioning',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
