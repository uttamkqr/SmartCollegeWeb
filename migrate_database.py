"""
Database Migration Script
Adds missing columns to existing attendance table
"""
import mysql.connector
from db_config import get_connection


def migrate_attendance_table():
    """Add missing columns to attendance table"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("🔄 DATABASE MIGRATION - Attendance Table")
        print("=" * 60)

        # Check if marked_by column exists
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_SCHEMA = DATABASE()
                         AND TABLE_NAME = 'attendance'
                         AND COLUMN_NAME = 'marked_by'
        """)

        marked_by_exists = cursor.fetchone()[0] > 0

        # Check if method column exists
        cursor.execute("""
                       SELECT COUNT(*)
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_SCHEMA = DATABASE()
                         AND TABLE_NAME = 'attendance'
                         AND COLUMN_NAME = 'method'
        """)

        method_exists = cursor.fetchone()[0] > 0

        changes_made = False

        # Add marked_by column if not exists
        if not marked_by_exists:
            print("\n📝 Adding 'marked_by' column...")
            cursor.execute("""
                           ALTER TABLE attendance
                               ADD COLUMN marked_by VARCHAR(50) DEFAULT 'System'
            """)
            conn.commit()
            print("✅ Added 'marked_by' column successfully")
            changes_made = True
        else:
            print("\n✓ 'marked_by' column already exists")

        # Add method column if not exists
        if not method_exists:
            print("\n📝 Adding 'method' column...")
            cursor.execute("""
                           ALTER TABLE attendance
                               ADD COLUMN method VARCHAR(20) DEFAULT 'Face'
            """)
            conn.commit()
            print("✅ Added 'method' column successfully")
            changes_made = True
        else:
            print("✓ 'method' column already exists")

        # Show current table structure
        print("\n📋 Current Attendance Table Structure:")
        cursor.execute("""
                       SELECT COLUMN_NAME, COLUMN_TYPE, IS_NULLABLE, COLUMN_DEFAULT
                       FROM INFORMATION_SCHEMA.COLUMNS
                       WHERE TABLE_SCHEMA = DATABASE()
                         AND TABLE_NAME = 'attendance'
                       ORDER BY ORDINAL_POSITION
        """)

        columns = cursor.fetchall()
        print("\n" + "-" * 60)
        for col in columns:
            col_name, col_type, nullable, default = col
            print(f"  {col_name:<15} {col_type:<20} NULL:{nullable} DEFAULT:{default}")
        print("-" * 60)

        if changes_made:
            print("\n✅ Migration completed successfully!")
            print("🎉 Database schema is now up to date")
        else:
            print("\n✓ Database schema is already up to date")

        print("=" * 60 + "\n")

        cursor.close()
        conn.close()
        return True

    except mysql.connector.Error as err:
        print(f"\n❌ Migration Error: {err}")
        if conn:
            conn.rollback()
        return False
    except Exception as e:
        print(f"\n❌ Unexpected Error: {e}")
        return False
    finally:
        if conn:
            try:
                cursor.close()
                conn.close()
            except:
                pass


def check_database_health():
    """Check overall database health"""
    conn = None
    try:
        conn = get_connection()
        cursor = conn.cursor()

        print("\n" + "=" * 60)
        print("🏥 DATABASE HEALTH CHECK")
        print("=" * 60)

        # Check students table
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        print(f"\n✅ Students Table: {student_count} records")

        # Check attendance table
        cursor.execute("SELECT COUNT(*) FROM attendance")
        attendance_count = cursor.fetchone()[0]
        print(f"✅ Attendance Table: {attendance_count} records")

        # Check admin_users table
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        admin_count = cursor.fetchone()[0]
        print(f"✅ Admin Users Table: {admin_count} records")

        # Check attendance_logs table
        cursor.execute("SELECT COUNT(*) FROM attendance_logs")
        logs_count = cursor.fetchone()[0]
        print(f"✅ Attendance Logs Table: {logs_count} records")

        print("\n" + "=" * 60)
        print("✅ All tables are healthy!")
        print("=" * 60 + "\n")

        cursor.close()
        conn.close()
        return True

    except Exception as e:
        print(f"\n❌ Health Check Error: {e}\n")
        return False
    finally:
        if conn:
            try:
                cursor.close()
                conn.close()
            except:
                pass


def main():
    """Run migration"""
    print("\n🚀 SMART ATTENDANCE SYSTEM - DATABASE MIGRATION")
    print("=" * 60)

    # Run migration
    if migrate_attendance_table():
        # Check health after migration
        check_database_health()

        print("\n💡 NEXT STEPS:")
        print("   1. Run test script: python test_attendance.py")
        print("   2. Start application: python app.py")
        print("   3. Access at: http://localhost:5000")
        print("\n" + "=" * 60 + "\n")
    else:
        print("\n❌ Migration failed. Please check the error above.")
        print("   - Make sure MySQL is running")
        print("   - Check database credentials in .env file")
        print("   - Verify database name is correct\n")


if __name__ == "__main__":
    main()
