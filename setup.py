#!/usr/bin/env python3
"""
SDG4 AI Tutor Django Setup Script
Run this script to set up the Django version of the application.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, check=True):
    """Run shell command"""
    print(f"Running: {command}")
    result = subprocess.run(command, shell=True, check=check)
    return result.returncode == 0


def setup_django_app():
    """Setup Django application"""
    print("🚀 Setting up SDG4 AI Tutor (Django Version)...")
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # Create virtual environment
    print("\n📦 Creating virtual environment...")
    if not os.path.exists("venv"):
        run_command(f"{sys.executable} -m venv venv")
    
    # Determine activation script
    if os.name == 'nt':  # Windows
        pip_path = "venv\\Scripts\\pip"
        python_path = "venv\\Scripts\\python"
    else:  # Unix/Linux/Mac
        pip_path = "venv/bin/pip"
        python_path = "venv/bin/python"
    
    # Install requirements
    print("\n📚 Installing dependencies...")
    run_command(f"{pip_path} install -r requirements.txt")
    
    # Setup environment file
    print("\n⚙️ Setting up environment...")
    if not os.path.exists(".env"):
        shutil.copy(".env.example", ".env")
        print("✅ Created .env file from example")
        print("🔧 Please edit .env file with your API keys and database settings")
    
    # Create necessary directories
    os.makedirs("static/images", exist_ok=True)
    os.makedirs("media", exist_ok=True)
    os.makedirs("templates/registration", exist_ok=True)
    os.makedirs("templates/payments", exist_ok=True)
    
    print("\n🎉 Django setup complete!")
    print("\nNext steps:")
    print("1. Edit .env file with your API keys")
    print("2. Create MySQL database 'agroflow_db'")
    print("3. Run: python manage.py makemigrations")
    print("4. Run: python manage.py migrate")
    print("5. Run: python manage.py createsuperuser")
    print("6. Run: python manage.py runserver")
    print("\n🌐 Then visit: http://127.0.0.1:8000")
    print("🔧 Admin: http://127.0.0.1:8000/admin")


if __name__ == "__main__":
    setup_django_app()

