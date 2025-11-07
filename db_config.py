import mysql.connector
from mysql.connector import pooling
import os

# Create a connection pool for better performance
db_pool = pooling.MySQLConnectionPool(
    pool_name="smart_attendance_pool",
    pool_size=5,
    host=os.environ.get("DB_HOST", "localhost"),
    user=os.environ.get("DB_USER", "root"),
    password=os.environ.get("DB_PASSWORD", ""),
    database=os.environ.get("DB_NAME", "smart_attendance"),
    autocommit=False
)


def get_connection():
    """Get a connection from the pool"""
    try:
        return db_pool.get_connection()
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        raise


def init_database():
    """Initialize database tables if they don't exist"""
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # Create students table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS students
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           name
                           VARCHAR
                       (
                           255
                       ) NOT NULL,
                           roll_no VARCHAR
                       (
                           50
                       ) UNIQUE NOT NULL,
                           email VARCHAR
                       (
                           255
                       ) NOT NULL,
                           phone VARCHAR
                       (
                           20
                       ),
                           department VARCHAR
                       (
                           100
                       ),
                           image_path VARCHAR
                       (
                           500
                       ),
                           qr_code VARCHAR
                       (
                           500
                       ),
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
                           )
                       """)

        # Create attendance table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS attendance
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           student_id
                           INT
                           NOT
                           NULL,
                           date
                           DATE
                           NOT
                           NULL,
                           time
                           TIME
                           NOT
                           NULL,
                           status
                           ENUM
                       (
                           'Present',
                           'Absent',
                           'Late'
                       ) DEFAULT 'Present',
                           marked_by VARCHAR
                       (
                           50
                       ) DEFAULT 'System',
                           method VARCHAR
                       (
                           20
                       ) DEFAULT 'Face',
                           FOREIGN KEY
                       (
                           student_id
                       ) REFERENCES students
                       (
                           id
                       ) ON DELETE CASCADE,
                           UNIQUE KEY unique_attendance
                       (
                           student_id,
                           date
                       )
                           )
                       """)

        # Create admin users table
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS admin_users
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           username
                           VARCHAR
                       (
                           50
                       ) UNIQUE NOT NULL,
                           password_hash VARCHAR
                       (
                           255
                       ) NOT NULL,
                           email VARCHAR
                       (
                           255
                       ),
                           full_name VARCHAR
                       (
                           255
                       ),
                           role VARCHAR
                       (
                           50
                       ) DEFAULT 'admin',
                           created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                           )
                       """)

        # Create attendance logs table for detailed tracking
        cursor.execute("""
                       CREATE TABLE IF NOT EXISTS attendance_logs
                       (
                           id
                           INT
                           AUTO_INCREMENT
                           PRIMARY
                           KEY,
                           student_id
                           INT
                           NOT
                           NULL,
                           action
                           VARCHAR
                       (
                           50
                       ) NOT NULL,
                           timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                           ip_address VARCHAR
                       (
                           50
                       ),
                           user_agent TEXT,
                           FOREIGN KEY
                       (
                           student_id
                       ) REFERENCES students
                       (
                           id
                       ) ON DELETE CASCADE
                           )
                       """)

        conn.commit()
        print("Database tables initialized successfully")
    except mysql.connector.Error as err:
        print(f"Error creating tables: {err}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()
