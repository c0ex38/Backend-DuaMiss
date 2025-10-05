# Backend-DuaMiss

Django REST API backend for DuaMiss dashboard application.

## 🚀 Quick Start

### Local Development

1. **Clone & Setup**
```bash
git clone <repository-url>
cd Backend-DuaMiss
```

2. **Create Virtual Environment**
```bash
python -m venv .venv
source .venv/bin/activate  # Mac/Linux
# or
.venv\Scripts\activate  # Windows
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Environment Configuration**
```bash
cp .env.example .env
# Edit .env with your local settings
```

5. **Database Setup**
```bash
python manage.py migrate
python manage.py createsuperuser
```

6. **Run Development Server**
```bash
python manage.py runserver
```

Visit: http://localhost:8000/admin/

## 📁 Project Structure

```
Backend-DuaMiss/
├── dashboard_project/      # Main project settings
│   ├── settings.py        # Django configuration
│   ├── urls.py           # URL routing
│   └── wsgi.py           # WSGI config
├── users/                 # User management app
├── company/              # Company data app
├── product/              # Product management app
├── order/                # Order processing app
├── requirements.txt      # Python dependencies
├── .env.example         # Environment template
├── build.sh             # Render build script
├── render.yaml          # Render deployment config
└── DEPLOYMENT.md        # Deployment guide
```

## 🔧 Tech Stack

- **Framework:** Django 5.2.5
- **API:** Django REST Framework
- **Auth:** JWT (Simple JWT)
- **Database:** PostgreSQL (Supabase)
- **Server:** Gunicorn
- **Static Files:** WhiteNoise

## 📦 Key Dependencies

```
Django==5.2.5
djangorestframework==3.16.1
djangorestframework-simplejwt==5.5.1
django-environ==0.12.0
django-cors-headers==4.7.0
psycopg2-binary==2.9.10
gunicorn==23.0.0
whitenoise>=6.6
```

## 🌐 API Endpoints

### Authentication
- `POST /api/users/register/` - User registration
- `POST /api/users/login/` - User login (JWT)
- `POST /api/users/token/refresh/` - Refresh token

### Resources
- `/api/companies/` - Company CRUD
- `/api/products/` - Product CRUD
- `/api/orders/` - Order management

## 🔒 Environment Variables

Required environment variables (see `.env.example`):

```bash
SECRET_KEY=<django-secret-key>
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:3000
DATABASE_URL=postgresql://user:pass@host:5432/db
```

## 🚀 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed Render.com deployment instructions.

**Quick Deploy:**
```bash
# 1. Push to GitHub
git push origin main

# 2. Connect to Render.com
# 3. Environment variables will be set from render.yaml
# 4. Auto-deploy on push
```

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Check deployment readiness
python manage.py check --deploy

# Check migrations
python manage.py showmigrations
```

## 📝 Development Commands

```bash
# Create new app
python manage.py startapp appname

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Django shell
python manage.py shell
```

## 🔐 Security Features

- JWT Authentication
- CORS protection
- CSRF protection
- SSL/HTTPS enforcement (production)
- Secure cookies (production)
- HSTS headers (production)

## 📊 Database

**Local Development:** SQLite (fallback)
**Production:** PostgreSQL on Supabase

Connection pooling via PgBouncer (transaction mode).

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

[Your License Here]

## 👥 Team

DuaMiss Development Team

---

**Project Status:** 🟢 Active Development
**Last Updated:** October 2025
