# Django SDG4 Education Platform

## 🎓 Complete Django Application for SDG 4 (Quality Education)

This package contains a fully functional Django web application that provides AI-powered educational tutoring aligned with Sustainable Development Goal 4.

## 🚀 Features

- **AI-Powered Tutoring**: Integration with Hugging Face AI models
- **User Authentication**: Secure registration and login system with custom User model
- **Credit-Based System**: Pay-per-use AI interactions
- **Payment Processing**: IntaSend payment gateway integration
- **Responsive Design**: Modern Bootstrap-based interface
- **Security Features**: Rate limiting, CSRF protection, Content Security Policy
- **Admin Interface**: Full Django admin integration

## 📋 Prerequisites

- Python 3.8+
- MySQL Server
- Hugging Face API Token
- IntaSend Payment Gateway Account

## 🛠️ Installation

1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Database Setup**:
   ```bash
   python reset_django_db.py
   ```

3. **Run Tests**:
   ```bash
   python test_django_full.py
   ```

4. **Start Application**:
   ```bash
   python manage.py runserver
   ```

5. **Access Application**:
   Visit: http://127.0.0.1:8000

## 🔧 Configuration

### Development Settings
- Uses `sdg4_project/settings.py`
- DEBUG = True (normal for development)
- May show security warnings (expected)

### Production Settings
- Uses `sdg4_project/production_settings.py`
- DEBUG = False
- All security warnings resolved
- Production-ready configuration

## 👤 Default Users

- **Admin**: admin@sdg4.edu / admin123
- **Test**: test@example.com / test123

## 📊 Database Schema

- **Users**: Custom User model with credit management
- **AI Interactions**: AI tutoring session history
- **Payments**: Payment transaction records
- **Subscriptions**: Subscription plan management

## 🔒 Security Features

- Custom User model with password hashing
- CSRF protection
- Rate limiting (django-ratelimit)
- Content Security Policy headers
- Input validation and sanitization
- Production-ready security settings

## 💰 Monetization Strategy

- Credit-based AI interactions (1-3 credits per use)
- Subscription plans (Basic, Premium, Institutional)
- Payment gateway integration
- User credit management

## 🧪 Testing

Run comprehensive tests:
```bash
python test_django_full.py
python check_settings.py
```

## 📁 Project Structure

```
django_sdg4_education_platform/
├── sdg4_project/           # Django project settings
│   ├── __init__.py         # Project initialization
│   ├── settings.py         # Development settings
│   ├── production_settings.py # Production settings
│   ├── urls.py             # Main URL configuration
│   └── wsgi.py             # WSGI entry point
├── apps/                   # Django applications
│   ├── accounts/           # User management & models
│   ├── ai_tutor/           # AI integration
│   └── payments/           # Payment processing
├── templates/              # Django templates
├── static/                 # CSS, JS, images
├── manage.py               # Django management
├── requirements.txt        # Python dependencies
└── README.md              # This file
```

## 🎯 SDG 4 Alignment

This application directly supports Sustainable Development Goal 4 by:
- Providing quality educational content through AI
- Making education accessible through technology
- Supporting lifelong learning opportunities
- Promoting inclusive and equitable education

## 🚀 Production Deployment

1. **Use Production Settings**:
   ```bash
   python manage.py runserver --settings=sdg4_project.production_settings
   ```

2. **Set Environment Variables**:
   - SECRET_KEY
   - Database credentials
   - Email settings
   - API keys

3. **Configure Web Server**:
   - Nginx/Apache
   - Gunicorn/uWSGI
   - SSL/HTTPS

## 📞 Support

For technical support or questions about the application, please refer to the documentation or contact the development team.

---
**Package Created**: 2025-09-01 20:44:40
**Total Files**: 37
