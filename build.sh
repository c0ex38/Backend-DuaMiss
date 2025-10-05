#!/usr/bin/env bash
# exit on error
set -o errexit

echo "🔧 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "📦 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️  Running migrations..."
python manage.py migrate

echo "👤 Creating default users if not exist..."
python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

# Admin user
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@duamiss.com', 'DuaMiss2025!Admin')
    print('✅ Admin user created: admin / DuaMiss2025!Admin')
else:
    print('ℹ️  Admin user already exists')

# Test user (same as local)
if not User.objects.filter(username='test').exists():
    User.objects.create_superuser('test', 'test@duamiss.com', 'tester.1')
    print('✅ Test user created: test / tester.1')
else:
    print('ℹ️  Test user already exists')

print(f'📊 Total users in database: {User.objects.count()}')
END

echo "✅ Build completed successfully!"
