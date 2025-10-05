#!/usr/bin/env bash
# Supabase bağlantı testi

echo "🔍 Testing Supabase connection..."
echo ""

# Database connection test
echo "1️⃣ Testing database connection..."
python manage.py check --database default

if [ $? -eq 0 ]; then
    echo "✅ Database connection OK"
else
    echo "❌ Database connection FAILED"
    exit 1
fi

echo ""
echo "2️⃣ Checking users in database..."
python manage.py shell << END
from users.models import CustomUser

try:
    user_count = CustomUser.objects.count()
    print(f"✅ Found {user_count} users in database")
    
    if user_count > 0:
        print("\n📋 Users:")
        for user in CustomUser.objects.all()[:5]:
            print(f"   - {user.username} ({user.email})")
    else:
        print("⚠️  No users found in database!")
except Exception as e:
    print(f"❌ Error: {e}")
END

echo ""
echo "3️⃣ Testing authentication..."
python manage.py shell << END
from django.contrib.auth import authenticate
from users.models import CustomUser

# Test ile bir user var mı kontrol et
if CustomUser.objects.filter(username='test').exists():
    user = authenticate(username='test', password='tester.1')
    if user:
        print("✅ Authentication works! User 'test' authenticated successfully")
    else:
        print("❌ Authentication failed - wrong password or user inactive")
else:
    print("⚠️  User 'test' not found in database")
    print(f"Available users: {list(CustomUser.objects.values_list('username', flat=True)[:5])}")
END

echo ""
echo "✅ Test completed!"
