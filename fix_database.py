#!/usr/bin/env python
"""
Database Fix Script
Adds missing columns to existing tables
"""

import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()


def fix_database():
    """Fix database schema by adding missing columns"""
    try:
        # Connect to database
        conn = mysql.connector.connect(
            host=os.environ.get("DB_HOST", "localhost"),
            user=os.environ.get("DB_USER", "root"),
            password=os.environ.get("DB_PASSWORD", ""),
            database=os.environ.get("DB_NAME", "smart_attendance")
        )

        cursor = conn.cursor()

        print("🔧 Fixing database schema...\n")

        # Check and add missing columns to students table
        print("1. Checking students table...")

        # Get current columns
        cursor.execute("DESCRIBE students")
        existing_columns = [row[0] for row in cursor.fetchall()]
        print(f"   Current columns: {existing_columns}")

        # Add phone column if missing
        if 'phone' not in existing_columns:
            print("   ➕ Adding 'phone' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN phone VARCHAR(20) AFTER email
            """)
            print("   ✅ Added 'phone' column")
        else:
            print("   ✅ 'phone' column exists")

        # Add department column if missing
        if 'department' not in existing_columns:
            print("   ➕ Adding 'department' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN department VARCHAR(100) AFTER phone
            """)
            print("   ✅ Added 'department' column")
        else:
            print("   ✅ 'department' column exists")

        # Add image_path column if missing
        if 'image_path' not in existing_columns:
            print("   ➕ Adding 'image_path' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN image_path VARCHAR(500) AFTER department
            """)
            print("   ✅ Added 'image_path' column")
        else:
            print("   ✅ 'image_path' column exists")

        # Add qr_code column if missing
        if 'qr_code' not in existing_columns:
            print("   ➕ Adding 'qr_code' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN qr_code VARCHAR(500) AFTER image_path
            """)
            print("   ✅ Added 'qr_code' column")
        else:
            print("   ✅ 'qr_code' column exists")

        # Add timestamps if missing
        if 'created_at' not in existing_columns:
            print("   ➕ Adding 'created_at' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            """)
            print("   ✅ Added 'created_at' column")
        else:
            print("   ✅ 'created_at' column exists")

        if 'updated_at' not in existing_columns:
            print("   ➕ Adding 'updated_at' column...")
            cursor.execute("""
                           ALTER TABLE students
                               ADD COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
            """)
            print("   ✅ Added 'updated_at' column")
        else:
            print("   ✅ 'updated_at' column exists")

        # Commit changes
        conn.commit()

        # Show final structure
        print("\n2. Final students table structure:")
        cursor.execute("DESCRIBE students")
        for row in cursor.fetchall():
            print(f"   - {row[0]}: {row[1]}")

        print("\n✅ Database schema fixed successfully!")
        print("\nℹ️  You can now run: python app.py")

    except mysql.connector.Error as err:
        print(f"\n❌ Database Error: {err}")
        if "Unknown database" in str(err):
            print("\n⚠️  Database doesn't exist! Create it first:")
            print("   mysql -u root -p")
            print("   CREATE DATABASE smart_attendance;")
            print("   EXIT;")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()


if __name__ == "__main__":
    print("=" * 60)
    print("DATABASE SCHEMA FIX TOOL")
    print("=" * 60)
    print()
    fix_database()
