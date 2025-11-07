-- Smart College Dashboard Database Setup
-- Run this file with: mysql -u root -p < create_database.sql

-- Create database
CREATE
DATABASE IF NOT EXISTS smart_attendance;

-- Use the database
USE
smart_attendance;

-- Show success message
SELECT 'Database smart_attendance created successfully!' AS Message;

-- Show all databases
SHOW
DATABASES;
