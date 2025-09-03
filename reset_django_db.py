#!/usr/bin/env python3
"""
Reset Django database and start fresh
"""

import os
import sys
import django
import pymysql
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdg4_project.settings')
    django.setup()

def reset_database():
    """Reset the database completely"""
    print("🗑️ Resetting database...")
    
    try:
        # Connect to MySQL and drop all tables
        connection = pymysql.connect(
            host='localhost',
            port=3306,
            user='root',
            password='password',
            database='agroflow_db'
        )
        
        cursor = connection.cursor()
        
        # Disable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
        
        # Get all tables
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()
        
        # Drop each table
        for table in tables:
            table_name = table[0]
            print(f"  - Dropping {table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        # Re-enable foreign key checks
        cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
        
        connection.commit()
        cursor.close()
        connection.close()
        
        print("✅ Database reset successfully")
        return True
        
    except Exception as e:
        print(f"❌ Database reset failed: {e}")
        return False

def create_migrations():
    """Create fresh migrations"""
    print("📝 Creating fresh migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
        print("✅ Migrations created successfully")
        return True
    except Exception as e:
        print(f"❌ Migration creation failed: {e}")
        return False

def run_migrations():
    """Run migrations on clean database"""
    print("🗄️ Running migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create superuser"""
    print("👤 Creating superuser...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.create_superuser(
            username='admin',
            email='admin@sdg4.edu',
            password='admin123',
            credits=1000
        )
        print(f"✅ Superuser created: {user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Superuser creation failed: {e}")
        return False

def create_sample_data():
    """Create sample data"""
    print("📊 Creating sample data...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='test123',
            credits=50
        )
        print(f"✅ Test user created: {user.email}")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Django Database Reset & Setup")
    print("=" * 40)
    
    # Setup Django
    setup_django()
    
    # Reset database
    if not reset_database():
        return
    
    # Create migrations
    if not create_migrations():
        return
    
    # Run migrations
    if not run_migrations():
        return
    
    # Create superuser
    if not create_superuser():
        return
    
    # Create sample data
    if not create_sample_data():
        return
    
    print("\n🎉 Django database setup completed successfully!")
    print("\n📋 Login Credentials:")
    print("  - Admin: admin@sdg4.edu / admin123")
    print("  - Test: test@example.com / test123")
    
    print("\n🚀 To start Django server:")
    print("  python manage.py runserver")
    print("  Then visit: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
