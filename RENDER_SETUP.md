# 🔐 Render.com Environment Variables Setup

## ⚡ HIZLI KURULUM

Render Dashboard'a gidin ve bu değişkenleri **TAM OLARAK** ekleyin:

---

## 📋 Environment Variables

### 1. SECRET_KEY
```
SECRET_KEY
```
**Value:** Render otomatik generate edecek (veya kendi ürettiğinizi kullanın)

**Nasıl üretilir:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 2. DEBUG
```
DEBUG
```
**Value:**
```
False
```

---

### 3. DATABASE_URL (SUPABASE SESSION MODE)
```
DATABASE_URL
```
**Value:**
```
postgresql://postgres.gcuelkevdajcuiysyqgq:nchIWG9F8LfTVyYr@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

⚠️ **ÇOK ÖNEMLİ:** Port **6543** olmalı (5432 DEĞİL!)

---

### 4. ALLOWED_HOSTS
```
ALLOWED_HOSTS
```
**Value:**
```
.onrender.com,localhost
```

⚠️ **DİKKAT:** Virgülden sonra BOŞLUK YOK!

---

### 5. CORS_ALLOWED_ORIGINS
```
CORS_ALLOWED_ORIGINS
```
**Value:**
```
https://frontend-dua-miss.vercel.app,https://frontend-duamiss.onrender.com
```

⚠️ **DİKKAT:** 
- HTTPS kullan (HTTP değil!)
- Virgülden sonra BOŞLUK YOK!

---

### 6. CSRF_TRUSTED_ORIGINS
```
CSRF_TRUSTED_ORIGINS
```
**Value:**
```
https://backend-duamiss.onrender.com,https://*.onrender.com,https://*.vercel.app
```

⚠️ **DİKKAT:** Virgülden sonra BOŞLUK YOK!

---

## 🚀 Adım Adım Ekleme

1. **Render Dashboard'a git:**
   ```
   https://dashboard.render.com
   ```

2. **Service'inizi seçin:** `backend-duamiss`

3. **Environment tab'ına tıklayın**

4. **Her değişken için:**
   - "Add Environment Variable" tıkla
   - Key'i yukarıdaki gibi gir
   - Value'yu KOPYALA-YAPIŞTIR yap (elle yazma!)
   - "Add" tıkla

5. **Tüm değişkenleri ekledikten sonra:**
   - "Save Changes" tıkla
   - Otomatik redeploy başlayacak

---

## ✅ Kontrol Listesi

Render Environment'ta şunlar olmalı:

- ✅ SECRET_KEY (50+ karakter random string)
- ✅ DEBUG=False
- ✅ DATABASE_URL (port 6543 ile)
- ✅ ALLOWED_HOSTS (.onrender.com,localhost)
- ✅ CORS_ALLOWED_ORIGINS (https://... ile başlamalı)
- ✅ CSRF_TRUSTED_ORIGINS (https://... ile başlamalı)

---

## 🧪 Deploy Sonrası Test

Deploy tamamlandıktan sonra (2-5 dakika):

### 1. Health Check
```bash
curl https://backend-duamiss.onrender.com/
# Beklenen: "Backend OK"
```

### 2. API Root
```bash
curl https://backend-duamiss.onrender.com/api/
# Beklenen: 200 OK
```

### 3. Admin Panel (Browser'da)
```
https://backend-duamiss.onrender.com/admin/
# Beklenen: Login sayfası (500 DEĞİL!)
```

### 4. Token Login
```bash
curl -X POST https://backend-duamiss.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"test","password":"tester.1"}'

# Beklenen: {"refresh":"...","access":"..."}
```

---

## 🔧 Sorun mu var?

### Hala 500 hatası alıyorsan:

1. **Render Logs'u kontrol et:**
   ```
   Dashboard → backend-duamiss → Logs
   ```

2. **Shell'den database test et:**
   ```
   Dashboard → backend-duamiss → Shell → "Launch Shell"
   
   python manage.py check --database default
   python manage.py showmigrations
   ```

3. **User oluştur (eğer yoksa):**
   ```bash
   python manage.py shell
   >>> from users.models import CustomUser
   >>> CustomUser.objects.create_superuser('test', 'test@test.com', 'tester.1')
   >>> exit()
   ```

---

## 📝 Notlar

- **Port 6543:** Supabase Session mode (Django uyumlu)
- **Port 5432:** Transaction mode (Django ile ÇALIŞMAZ!)
- **Boşluk yok:** Virgülden sonra boşluk eklemeyin
- **HTTPS zorunlu:** Production'da http:// kullanmayın

---

**Hazır! 🎉** 

Environment'ı kaydedin ve 2-5 dakika sonra test edin!
