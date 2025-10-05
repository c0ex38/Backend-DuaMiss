#!/usr/bin/env bash
# Render.com Shell'de çalıştırılacak debug script

echo "=== 🔍 Django Production Debug Script ==="
echo ""

echo "1️⃣ Checking Django installation..."
python --version
echo ""

echo "2️⃣ Checking database connection..."
python manage.py check --database default
echo ""

echo "3️⃣ Checking migrations status..."
python manage.py showmigrations
echo ""

echo "4️⃣ Checking if tables exist..."
python manage.py dbshell << EOF
\dt
\q
EOF
echo ""

echo "5️⃣ Checking CustomUser count..."
python manage.py shell << EOF
from users.models import CustomUser
print(f"Total users: {CustomUser.objects.count()}")
if CustomUser.objects.exists():
    print(f"First user: {CustomUser.objects.first().username}")
EOF
echo ""

echo "6️⃣ Testing JWT token generation..."
python manage.py shell << EOF
from users.models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

user = CustomUser.objects.first()
if user:
    refresh = RefreshToken.for_user(user)
    print(f"✅ Token generated successfully")
    print(f"Access token: {str(refresh.access_token)[:50]}...")
else:
    print("❌ No users found!")
EOF
echo ""

echo "7️⃣ Checking settings..."
python manage.py diffsettings --all | grep -E "(ALLOWED_HOSTS|DEBUG|DATABASE|CORS|CSRF)"
echo ""

echo "=== ✅ Debug script completed ==="
