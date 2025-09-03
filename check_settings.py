#!/usr/bin/env python3
"""
Check Django settings for development vs production
"""

import subprocess
import sys

def check_settings(settings_module):
    """Check Django settings with specific module"""
    try:
        result = subprocess.run([
            'python', 'manage.py', 'check', '--deploy', 
            f'--settings={settings_module}'
        ], capture_output=True, text=True, cwd='.')
        
        if result.returncode == 0:
            print(f"✅ {settings_module}: No issues found")
            return True
        else:
            print(f"❌ {settings_module}: Issues found")
            print(result.stdout)
            return False
            
    except Exception as e:
        print(f"❌ Error checking {settings_module}: {e}")
        return False

def main():
    """Main function"""
    print("🔍 Django Settings Check - Development vs Production")
    print("=" * 60)
    
    # Check development settings
    print("\n📋 Checking Development Settings...")
    dev_result = check_settings('sdg4_project.settings')
    
    # Check production settings
    print("\n📋 Checking Production Settings...")
    prod_result = check_settings('sdg4_project.production_settings')
    
    print("\n📊 Summary:")
    print(f"  - Development: {'✅ Clean' if dev_result else '❌ Has warnings'}")
    print(f"  - Production: {'✅ Clean' if prod_result else '❌ Has issues'}")
    
    if not dev_result:
        print("\n💡 Development warnings are normal and expected.")
        print("   These are security recommendations for production deployment.")
    
    if prod_result:
        print("\n🎉 Production settings are production-ready!")
        print("   All security warnings have been resolved.")
    
    print("\n🚀 To use production settings:")
    print("   python manage.py runserver --settings=sdg4_project.production_settings")
    print("   export DJANGO_SETTINGS_MODULE=sdg4_project.production_settings")

if __name__ == "__main__":
    main()
