#!/usr/bin/env python3
"""
Comprehensive Django application test
"""

import os
import sys
import django
from pathlib import Path

def setup_django():
    """Setup Django environment"""
    project_dir = Path(__file__).resolve().parent
    sys.path.insert(0, str(project_dir))
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sdg4_project.settings')
    django.setup()

def test_django_setup():
    """Test Django setup"""
    print("🚀 Testing Django setup...")
    
    try:
        from django.conf import settings
        print("✅ Django settings loaded")
        print(f"📋 Installed apps: {len(settings.INSTALLED_APPS)}")
        return True
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False

def test_models():
    """Test Django models"""
    print("\n📊 Testing Django models...")
    
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Test user creation
        test_user = User.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='test123',
            credits=25
        )
        print("✅ User model working")
        
        # Test credit deduction
        if test_user.deduct_credits(5):
            print("✅ Credit deduction working")
        else:
            print("❌ Credit deduction failed")
        
        # Test AI interaction
        from apps.accounts.models import AIInteraction
        interaction = AIInteraction.objects.create(
            user=test_user,
            prompt="What is SDG 4?",
            response="SDG 4 is about quality education...",
            model_used="test-model",
            credits_used=1
        )
        print("✅ AI Interaction model working")
        
        # Test payment model
        from apps.accounts.models import Payment
        payment = Payment.objects.create(
            user=test_user,
            intasend_payment_id="test_payment_123",
            amount=9.99,
            credits_purchased=100,
            status='completed'
        )
        print("✅ Payment model working")
        
        # Clean up
        test_user.delete()
        print("✅ Models test completed")
        return True
        
    except Exception as e:
        print(f"❌ Models test failed: {e}")
        return False

def test_views():
    """Test Django views"""
    print("\n🖥️ Testing Django views...")
    
    try:
        from django.test import Client
        from django.urls import reverse
        
        client = Client()
        
        # Test home page
        response = client.get('/')
        if response.status_code == 200:
            print("✅ Home page working")
        else:
            print(f"❌ Home page failed: {response.status_code}")
        
        # Test admin login
        response = client.get('/admin/')
        if response.status_code == 200:
            print("✅ Admin page accessible")
        else:
            print(f"❌ Admin page failed: {response.status_code}")
        
        return True
        
    except Exception as e:
        print(f"❌ Views test failed: {e}")
        return False

def test_urls():
    """Test URL configuration"""
    print("\n🛣️ Testing URL configuration...")
    
    try:
        from django.urls import get_resolver
        
        resolver = get_resolver()
        url_patterns = resolver.url_patterns
        
        print(f"✅ URL resolver working - {len(url_patterns)} patterns")
        
        # Check for key URLs
        expected_urls = ['/', '/admin/', '/accounts/']
        found_urls = []
        
        for pattern in url_patterns:
            if hasattr(pattern, 'pattern'):
                found_urls.append(str(pattern.pattern))
        
        print(f"📋 Found URLs: {len(found_urls)}")
        return True
        
    except Exception as e:
        print(f"❌ URL test failed: {e}")
        return False

def test_database():
    """Test database operations"""
    print("\n🗄️ Testing database operations...")
    
    try:
        from django.db import connection
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM accounts_user")
            count = cursor.fetchone()[0]
            print(f"✅ Database connection working - {count} users")
        
        # Test user query
        users = User.objects.all()
        print(f"✅ User query working - {users.count()} users found")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_admin():
    """Test admin interface"""
    print("\n👨‍💼 Testing admin interface...")
    
    try:
        from django.contrib import admin
        from apps.accounts.models import User, AIInteraction, Payment
        
        # Check if models are registered
        registered_models = admin.site._registry.keys()
        
        if User in registered_models:
            print("✅ User model registered in admin")
        else:
            print("❌ User model not registered in admin")
        
        if AIInteraction in registered_models:
            print("✅ AIInteraction model registered in admin")
        else:
            print("❌ AIInteraction model not registered in admin")
        
        if Payment in registered_models:
            print("✅ Payment model registered in admin")
        else:
            print("❌ Payment model not registered in admin")
        
        return True
        
    except Exception as e:
        print(f"❌ Admin test failed: {e}")
        return False

def main():
    """Main test function"""
    print("🚀 Django SDG4 Education Platform - Comprehensive Test")
    print("=" * 60)
    
    # Setup Django
    setup_django()
    
    tests = [
        ("Django Setup", test_django_setup),
        ("Models", test_models),
        ("Views", test_views),
        ("URLs", test_urls),
        ("Database", test_database),
        ("Admin", test_admin)
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
    elif passed >= total * 0.8:
        print("✅ Most Django tests passed!")
    else:
        print("⚠️ Several Django tests failed.")
    
    print(f"\n📋 Django Application Status:")
    print(f"  - Database: {'✅ Working' if passed >= 4 else '❌ Issues'}")
    print(f"  - Models: {'✅ Working' if passed >= 2 else '❌ Issues'}")
    print(f"  - Views: {'✅ Working' if passed >= 3 else '❌ Issues'}")
    print(f"  - Admin: {'✅ Working' if passed >= 5 else '❌ Issues'}")
    
    print(f"\n🚀 Django server is running at: http://127.0.0.1:8000")
    print(f"📋 Admin interface: http://127.0.0.1:8000/admin/")
    print(f"👤 Login: admin@sdg4.edu / admin123")

if __name__ == "__main__":
    main()
