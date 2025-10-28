-- Add Users Script for Qube.AI
-- This script adds Admin (password: Admin) and sadiq (password: admin)

-- Delete existing users to start fresh
DELETE FROM users;

-- Add Admin user with password "Admin" (capital A)
INSERT INTO users (username, password_hash, role) 
VALUES ('Admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeY5GyYzVEpTGzGO', 'admin');

-- Add sadiq user with password "admin" (lowercase)
INSERT INTO users (username, password_hash, role) 
VALUES ('sadiq', '$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW', 'admin');

-- Verify users were created
SELECT id, username, role, created_at FROM users ORDER BY id;

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Users added successfully!';
    RAISE NOTICE 'Admin credentials: Username=Admin, Password=Admin';
    RAISE NOTICE 'Sadiq credentials: Username=sadiq, Password=admin';
END $$;