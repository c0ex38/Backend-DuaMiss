#!/usr/bin/env bash
# Supabase bağlantı testi - Manuel parametrelerle

echo "🔍 Testing Supabase Session Mode Connection (Port 6543)..."
echo ""

# Connection parameters
export DB_USER="postgres.gcuelkevdajcuiysyqgq"
export DB_PASSWORD="nchIWG9F8LfTVyYr"  # Supabase password'ünüzü buraya yazın
export DB_HOST="aws-1-eu-central-1.pooler.supabase.com"
export DB_PORT="6543"
export DB_NAME="postgres"

# Construct connection string
export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo "📋 Connection Details:"
echo "   Host: ${DB_HOST}"
echo "   Port: ${DB_PORT}"
echo "   Database: ${DB_NAME}"
echo "   User: ${DB_USER}"
echo ""

# Test 1: psycopg2 bağlantısı
echo "1️⃣ Testing raw psycopg2 connection..."
python3 << END
import psycopg2
import os

try:
    conn = psycopg2.connect(
        host=os.environ['DB_HOST'],
        port=os.environ['DB_PORT'],
        dbname=os.environ['DB_NAME'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASSWORD'],
        sslmode='require',
        connect_timeout=10
    )
    
    cursor = conn.cursor()
    cursor.execute('SELECT version();')
    version = cursor.fetchone()
    print(f"✅ Connection successful!")
    print(f"   PostgreSQL version: {version[0][:50]}...")
    
    cursor.close()
    conn.close()
    print("✅ Connection closed successfully")
    
except Exception as e:
    print(f"❌ Connection failed: {e}")
    exit(1)
END

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ psycopg2 connection test FAILED"
    echo "Check your credentials and make sure Supabase allows connections"
    exit 1
fi

echo ""
echo "2️⃣ Testing Django database connection..."
python manage.py check --database default

if [ $? -eq 0 ]; then
    echo "✅ Django database connection OK"
else
    echo "❌ Django database connection FAILED"
    exit 1
fi

echo ""
echo "3️⃣ Checking migrations status..."
python manage.py showmigrations | head -20

echo ""
echo "4️⃣ Checking users in database..."
python manage.py shell << END
from users.models import CustomUser

try:
    user_count = CustomUser.objects.count()
    print(f"✅ Found {user_count} users in database")
    
    if user_count > 0:
        print("\n📋 Users:")
        for user in CustomUser.objects.all()[:10]:
            print(f"   - {user.username} ({user.email}) [Active: {user.is_active}]")
    else:
        print("⚠️  No users found in database!")
        print("Run: python manage.py createsuperuser")
except Exception as e:
    print(f"❌ Error: {e}")
END

echo ""
echo "✅ All tests completed successfully!"
echo ""
echo "📝 Next steps:"
echo "   1. If no users found, create one:"
echo "      python manage.py createsuperuser"
echo ""
echo "   2. Test login from terminal:"
echo "      curl -X POST http://localhost:8000/api/token/ \\"
echo "        -H 'Content-Type: application/json' \\"
echo "        -d '{\"username\":\"test\",\"password\":\"tester.1\"}'"
