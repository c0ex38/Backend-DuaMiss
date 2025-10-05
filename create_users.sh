#!/usr/bin/env bash
# Render Shell'de çalıştırılacak - Superuser oluşturur

echo "🔧 Creating superuser for production..."

python manage.py shell << END
from django.contrib.auth import get_user_model
User = get_user_model()

# Admin user oluştur
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        username='admin',
        email='admin@duamiss.com',
        password='DuaMiss2025!Admin'
    )
    print('✅ Admin user created!')
    print('   Username: admin')
    print('   Password: DuaMiss2025!Admin')
else:
    print('ℹ️  Admin user already exists')

# Test user oluştur
if not User.objects.filter(username='test').exists():
    User.objects.create_superuser(
        username='test',
        email='test@duamiss.com',
        password='tester.1'
    )
    print('✅ Test user created!')
    print('   Username: test')
    print('   Password: tester.1')
else:
    print('ℹ️  Test user already exists')

# Toplam user sayısı
print(f'\n📊 Total users: {User.objects.count()}')

END

echo "✅ Done!"
