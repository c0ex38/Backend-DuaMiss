# 🔧 Production 500 Error Troubleshooting

## ❌ Problem: Login ve Admin Panelde 500 Internal Server Error

### 🔍 Olası Nedenler ve Çözümler

## 1️⃣ **DATABASE_URL Sorunlu** (EN OLASI NEDEN)

### Kontrol:
Render Dashboard → Environment → `DATABASE_URL` değişkenini kontrol edin.

### Çözüm:
```bash
# Render otomatik PostgreSQL connection string'i şu formatta sağlar:
postgresql://USER:PASSWORD@HOST:PORT/DATABASE

# Eğer eksikse veya yanlışsa:
# 1. Render Dashboard → [Your Service] → Environment
# 2. DATABASE_URL'i kontrol et veya yeniden ekle
# 3. Redeploy
```

### Test:
```bash
# Render Shell'den database bağlantısını test et:
python manage.py dbshell
# Çalışırsa: ✅ DB bağlantısı OK
# Hata alırsa: ❌ DATABASE_URL yanlış
```

---

## 2️⃣ **Migrations Çalışmadı**

### Kontrol:
Render Logs → Build logs'ta `Running migrations...` çıktısını ara.

### Çözüm:
```bash
# Render Shell'den manuel migration:
python manage.py migrate

# Tüm migration durumunu kontrol:
python manage.py showmigrations

# Eğer applied görünmüyorsa:
python manage.py migrate --fake-initial
```

---

## 3️⃣ **SECRET_KEY Eksik veya Hatalı**

### Kontrol:
Render Dashboard → Environment → `SECRET_KEY` var mı?

### Çözüm:
```bash
# Yeni bir SECRET_KEY oluştur:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Çıktıyı kopyala ve Render'a ekle:
# Render Dashboard → Environment → SECRET_KEY = <kopyalanan-key>
# Save → Redeploy
```

---

## 4️⃣ **ALLOWED_HOSTS Hatalı**

### Kontrol:
Environment'ta `ALLOWED_HOSTS` doğru mu?

### Çözüm:
```bash
# Render Dashboard → Environment → ALLOWED_HOSTS:
backend-duamiss.onrender.com,.onrender.com

# ⚠️ DİKKAT:
# - Virgülle ayrılmalı (BOŞLUK YOK!)
# - .onrender.com wildcard olarak eklenebilir
# - localhost production'da OLMAMALI
```

---

## 5️⃣ **CORS Ayarları Eksik**

### Kontrol:
Frontend'den istek atarken CORS hatası var mı?

### Çözüm:
```bash
# Render Dashboard → Environment:
CORS_ALLOWED_ORIGINS=https://frontend-dua-miss.vercel.app,https://frontend-duamiss.onrender.com

# ⚠️ DİKKAT:
# - HTTPS kullan (HTTP değil!)
# - Boşluk YOK
# - Tüm frontend domain'leri ekle
```

---

## 6️⃣ **Static Files Sorunlu**

### Kontrol:
Render Logs → Build logs → `Collecting static files...` başarılı mı?

### Çözüm:
```bash
# Render Shell'den:
python manage.py collectstatic --no-input

# Eğer hata alırsan:
mkdir -p staticfiles
python manage.py collectstatic --no-input --clear
```

---

## 7️⃣ **Custom User Model Sorunu**

### Kontrol:
`AUTH_USER_MODEL = "users.CustomUser"` migration'ları yapıldı mı?

### Çözüm:
```bash
# Render Shell'den:
python manage.py migrate users
python manage.py migrate

# Superuser oluştur:
python manage.py createsuperuser
```

---

## 🚀 Hızlı Düzeltme Adımları

### Adım 1: Render Logs'u İncele
```
Render Dashboard → [Your Service] → Logs
```
Aradığınız şeyler:
- ❌ `ImproperlyConfigured: Set the DATABASE_URL environment variable`
- ❌ `OperationalError: FATAL: database "xyz" does not exist`
- ❌ `django.core.exceptions.ImproperlyConfigured`
- ❌ `relation "xyz" does not exist` (migration sorunları)

### Adım 2: Environment Variables'ı Kontrol Et
```
Render Dashboard → Environment → Kontrol edilecekler:

✅ SECRET_KEY (random string)
✅ DEBUG=False
✅ DATABASE_URL (postgresql://...)
✅ ALLOWED_HOSTS=backend-duamiss.onrender.com,.onrender.com
✅ CORS_ALLOWED_ORIGINS=https://frontend-dua-miss.vercel.app
✅ CSRF_TRUSTED_ORIGINS=https://backend-duamiss.onrender.com,https://*.vercel.app
```

### Adım 3: Manuel Deploy
```
Render Dashboard → Manual Deploy → Deploy latest commit
```

### Adım 4: Shell'den Test
```bash
# Render Dashboard → Shell açın:

# 1. Database bağlantısı test:
python manage.py check --database default

# 2. Migration durumu:
python manage.py showmigrations

# 3. Admin user var mı:
python manage.py shell
>>> from users.models import CustomUser
>>> CustomUser.objects.all()
>>> exit()

# 4. Token endpoint test:
python manage.py shell
>>> from rest_framework_simplejwt.tokens import RefreshToken
>>> from users.models import CustomUser
>>> user = CustomUser.objects.first()
>>> refresh = RefreshToken.for_user(user)
>>> print(f"Access: {refresh.access_token}")
>>> exit()
```

---

## 🐛 Debug Mode Geçici Aktif Etme (YALNIZCA TEST İÇİN!)

```bash
# ⚠️ SADECE SORUNU BULMAK İÇİN - SONRA KAPATIN!

# Render Dashboard → Environment:
DEBUG=True

# Save → Redeploy
# Hatayı gör → Screenshot al
# DEBUG=False yap → Redeploy
```

---

## 📊 Yaygın Hata Mesajları ve Çözümleri

### Hata: `relation "users_customuser" does not exist`
**Çözüm:**
```bash
python manage.py migrate users --fake-initial
python manage.py migrate
```

### Hata: `django.db.utils.OperationalError: FATAL: password authentication failed`
**Çözüm:**
DATABASE_URL yanlış → Render Dashboard'dan yeniden al

### Hata: `DisallowedHost at / Invalid HTTP_HOST header`
**Çözüm:**
ALLOWED_HOSTS'a domain ekle: `backend-duamiss.onrender.com`

### Hata: `CSRF verification failed`
**Çözüm:**
CSRF_TRUSTED_ORIGINS ekle: `https://backend-duamiss.onrender.com,https://*.vercel.app`

---

## ✅ Başarı Kontrolleri

Tüm bunları test edin:

1. **Backend Health:**
```bash
curl https://backend-duamiss.onrender.com/
# Beklenen: "Backend OK"
```

2. **API Endpoint:**
```bash
curl https://backend-duamiss.onrender.com/api/
# Beklenen: 200 OK (API root response)
```

3. **Admin Panel:**
```
https://backend-duamiss.onrender.com/admin/
# Beklenen: Login sayfası (500 değil!)
```

4. **Token Login:**
```bash
curl -X POST https://backend-duamiss.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123456"}'

# Beklenen: {"refresh":"...","access":"..."}
# Aldığınız: 500 ❌
```

---

## 🎯 En Olası Senaryonuz

Size göre muhtemelen:
1. ✅ Render deploy başarılı
2. ✅ Root endpoint (`/`) çalışıyor
3. ❌ `/api/token/` 500 veriyor
4. ❌ `/admin/` 500 veriyor

Bu, muhtemelen:
- **Database bağlantısı sorunlu** VEYA
- **Migrations çalışmamış** VEYA
- **CustomUser tablosu yok**

### Hızlı Fix:
```bash
# Render Shell:
python manage.py migrate
python manage.py createsuperuser --username admin --email admin@example.com

# Test:
python manage.py shell
>>> from users.models import CustomUser
>>> print(CustomUser.objects.count())
```

---

## 📞 Hala Çalışmıyorsa

1. **Render Logs'un Screenshot'unu al:**
   - Render Dashboard → Logs → Runtime logs
   - 500 hatası olan satırları bul

2. **Environment Variables Screenshot:**
   - Render Dashboard → Environment → Tüm değişkenler

3. **Manuel shell'den çalıştır:**
```bash
python manage.py check --deploy
```

Bu bilgilerle daha spesifik yardım edebilirim! 🚀
