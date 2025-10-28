-- Qube.AI Database Initialization Script
-- PostgreSQL Database Schema

-- Drop tables if they exist (for clean initialization)
DROP TABLE IF EXISTS project_settings CASCADE;
DROP TABLE IF EXISTS projects CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role VARCHAR(50) DEFAULT 'admin',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create projects table
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    domain VARCHAR(255) NOT NULL,
    brief TEXT NOT NULL,
    tech_stack TEXT,
    figma_url VARCHAR(500),
    figma_credentials_encrypted TEXT,
    compliance TEXT,
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create project_settings table
CREATE TABLE project_settings (
    id SERIAL PRIMARY KEY,
    project_id INTEGER UNIQUE REFERENCES projects(id) ON DELETE CASCADE,
    llm_provider VARCHAR(100) DEFAULT 'ollama',
    llm_model VARCHAR(100) DEFAULT 'llama2',
    api_key_encrypted TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create indexes for better query performance
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_projects_name ON projects(name);
CREATE INDEX idx_projects_created_by ON projects(created_by);
CREATE INDEX idx_project_settings_project_id ON project_settings(project_id);

-- Seed admin user
-- Password: Admin (hashed with bcrypt)
INSERT INTO users (username, password_hash, role) 
VALUES (
    'Admin',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5GyYzVEpTGzGO',
    'admin'
);

-- Success message
DO $$
BEGIN
    RAISE NOTICE 'Database initialized successfully!';
    RAISE NOTICE 'Default admin credentials: Username=Admin, Password=Admin';
END $$;