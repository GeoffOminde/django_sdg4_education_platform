#!/usr/bin/env python3
"""
Test Django setup and configuration
"""

import os
import sys
import django
from pathlib import Path

def test_django_setup():
    """Test Django setup and configuration"""
    print("🚀 Testing Django Setup...")
    
    try:
        # Add the project directory to Python path
        project_dir = Path(__file__).resolve().parent
        sys.path.insert(0, str(project_dir))
        
        # Set Django settings
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdg4_project.settings')
        
        # Configure Django
        django.setup()
        
        print("✅ Django setup successful")
        
        # Test imports
        from django.conf import settings
        print("✅ Django settings loaded")
        
        # Check installed apps
        print(f"📋 Installed apps: {len(settings.INSTALLED_APPS)}")
        for app in settings.INSTALLED_APPS:
            print(f"  - {app}")
        
        # Check database configuration
        print(f"📊 Database: {settings.DATABASES['default']['ENGINE']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_app_imports():
    """Test app imports"""
    print("\n📦 Testing app imports...")
    
    try:
        from apps.accounts.models import User, AIInteraction, Payment, Subscription
        print("✅ Accounts app imported")
        print("✅ AI Interaction model imported")
        print("✅ Payment model imported")
        print("✅ Subscription model imported")
        
        return True
        
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    print("\n🗄️ Testing database connection...")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            print("✅ Database connection successful")
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Django SDG4 Education Platform - Setup Test")
    print("=" * 50)
    
    tests = [
        ("Django Setup", test_django_setup),
        ("App Imports", test_app_imports),
        ("Database Connection", test_database_connection)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name} test...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} test passed")
        else:
            print(f"❌ {test_name} test failed")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All Django tests passed!")
    else:
        print("⚠️ Some tests failed. Check the issues above.")

if __name__ == "__main__":
    main()
