
-- Database setup for Flask-PostgreSQL application
-- Create a users table for user management
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create a posts table for content management
CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert sample users
INSERT INTO users (username, email) VALUES 
('admin', 'admin@example.com'),
('john_doe', 'john@example.com'),
('jane_smith', 'jane@example.com');

-- Insert sample posts
INSERT INTO posts (title, content, user_id) VALUES 
('Welcome to Flask App', 'This is the first post in our Flask-PostgreSQL application.', 1),
('Getting Started', 'Learn how to use this application effectively.', 1),
('User Guide', 'A comprehensive guide for new users.', 2);

-- Create an index for better query performance
CREATE INDEX IF NOT EXISTS idx_posts_user_id ON posts(user_id);
CREATE INDEX IF NOT EXISTS idx_posts_created_at ON posts(created_at);

-- Verify the setup
SELECT 'Users table:' as table_info;
SELECT * FROM users;
SELECT 'Posts table:' as table_info;
SELECT * FROM posts;

