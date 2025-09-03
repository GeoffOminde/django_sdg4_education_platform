#!/usr/bin/env python3
"""
Django database setup script
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    # Add the project directory to Python path
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    
    # Set Django settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdg4_project.settings')
    
    # Configure Django
    django.setup()

def create_migrations():
    """Create initial migrations"""
    print("📝 Creating Django migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'makemigrations', 'accounts'])
        execute_from_command_line(['manage.py', 'makemigrations', 'ai_tutor'])
        execute_from_command_line(['manage.py', 'makemigrations', 'payments'])
        print("✅ Migrations created successfully")
        return True
    except Exception as e:
        print(f"❌ Migration creation failed: {e}")
        return False

def run_migrations():
    """Run database migrations"""
    print("🗄️ Running database migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate'])
        print("✅ Migrations applied successfully")
        return True
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

def create_superuser():
    """Create a superuser"""
    print("👤 Creating superuser...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Check if superuser already exists
        if User.objects.filter(is_superuser=True).exists():
            print("✅ Superuser already exists")
            return True
        
        # Create superuser
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
        
        # Create test user
        if not User.objects.filter(email='test@example.com').exists():
            user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='test123',
                credits=50
            )
            print(f"✅ Test user created: {user.email}")
        
        print("✅ Sample data created successfully")
        return True
        
    except Exception as e:
        print(f"❌ Sample data creation failed: {e}")
        return False

def main():
    """Main function"""
    print("🚀 Django Database Setup")
    print("=" * 40)
    
    # Setup Django
    setup_django()
    
    # Create migrations
    if not create_migrations():
        print("❌ Failed to create migrations")
        return
    
    # Run migrations
    if not run_migrations():
        print("❌ Failed to run migrations")
        return
    
    # Create superuser
    create_superuser()
    
    # Create sample data
    create_sample_data()
    
    print("\n🎉 Django database setup completed!")
    print("\n📋 Login Credentials:")
    print("  - Admin: admin@sdg4.edu / admin123")
    print("  - Test: test@example.com / test123")
    
    print("\n🚀 To start Django server:")
    print("  python manage.py runserver")
    print("  Then visit: http://127.0.0.1:8000")

if __name__ == "__main__":
    main()
