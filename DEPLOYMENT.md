# Render.com Deployment Rehberi

Bu rehber, Django projesini Render.com'a deploy etmek için gereken adımları içerir.

## 📋 Ön Hazırlık

Projeye eklenen dosyalar:
- ✅ `build.sh` - Build script (migrations + collectstatic)
- ✅ `render.yaml` - Render konfigürasyon dosyası
- ✅ `runtime.txt` - Python versiyonu
- ✅ `requirements.txt` - Tüm bağımlılıklar (gunicorn, whitenoise, psycopg2-binary dahil)

## 🚀 Deployment Adımları

### 1. GitHub Repository Hazırlığı

```bash
# Tüm değişiklikleri commit edin
git add .
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### 2. Render.com Hesap ve Proje Oluşturma

1. [Render.com](https://render.com) hesabınıza giriş yapın (yoksa ücretsiz oluşturun)
2. Dashboard'dan **"New +"** → **"Blueprint"** seçin
3. GitHub repository'nizi bağlayın (Backend-DuaMiss)
4. `render.yaml` dosyası otomatik algılanacak

### 3. Environment Variables Ayarlama

Render Dashboard'da **Environment** sekmesinden şu değişkenleri ekleyin:

#### Zorunlu Değişkenler:
```
SECRET_KEY=<render otomatik oluşturacak>
DEBUG=False
DATABASE_URL=<render otomatik bağlayacak>
```

#### Domain/CORS Ayarları:
```
ALLOWED_HOSTS=backend-duamiss.onrender.com,.onrender.com

CORS_ALLOWED_ORIGINS=https://frontend-dua-miss.vercel.app,https://frontend-duamiss.onrender.com

CSRF_TRUSTED_ORIGINS=https://backend-duamiss.onrender.com,https://*.onrender.com,https://*.vercel.app,https://frontend-dua-miss.vercel.app
```

**⚠️ ÖNEMLİ:** 
- Her değişken virgülle ayrılmalı (boşluk yok!)
- HTTPS kullanın (HTTP değil)
- Frontend domain'inizi kendi URL'inizle değiştirin

### 4. Deploy Başlatma

1. **"Apply"** veya **"Create"** butonuna tıklayın
2. Render otomatik olarak:
   - PostgreSQL database oluşturacak
   - Python environment kuracak
   - Dependencies install edecek
   - Migrations çalıştıracak
   - Static files toplayacak
   - Gunicorn ile server başlatacak

### 5. İlk Deploy Sonrası

Deploy tamamlandığında:
- ✅ Backend URL: `https://backend-duamiss.onrender.com`
- ✅ Health check: `https://backend-duamiss.onrender.com/admin/`

## 🔧 Sorun Giderme

### Build Başarısız Olursa

1. **Logs'u kontrol edin:**
   - Render Dashboard → Logs sekmesi
   - Build ve Deploy loglarını inceleyin

2. **Yaygın sorunlar:**
   - `DATABASE_URL` eksik → Environment variables'ı kontrol edin
   - `build.sh` çalışmıyor → `chmod +x build.sh` yerel olarak yapıldığından emin olun
   - Migration hatası → Database bağlantısını kontrol edin

### Runtime Hataları

```bash
# Render Shell'den kontrol için:
python manage.py check --deploy
python manage.py showmigrations
```

## 📊 Database Management

### Migrations Çalıştırma
Otomatik: Her deploy'da `build.sh` içinde çalışır

### Manuel Migration (gerekirse)
Render Dashboard → Shell:
```bash
python manage.py migrate
python manage.py createsuperuser
```

## 🔒 Güvenlik Notları

Production ortamında aktif olan güvenlik ayarları:
- ✅ `DEBUG=False`
- ✅ SSL/HTTPS zorunlu
- ✅ Secure cookies
- ✅ HSTS headers
- ✅ CORS kontrolü
- ✅ CSRF protection

## 🌐 Frontend Bağlantısı

Frontend'den backend'e istek yaparken:
```javascript
const API_URL = 'https://backend-duamiss.onrender.com/api';

// Örnek request
fetch(`${API_URL}/users/login/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({ username, password })
});
```

## 📝 Sürekli Deployment (CD)

Artık her `main` branch'e push:
→ Render otomatik yeni deploy başlatır
→ Zero-downtime deployment

## 💰 Maliyet

**Free Plan:**
- Web Service: 750 saat/ay (1 instance için yeterli)
- PostgreSQL: 256 MB RAM, 1 GB storage
- Otomatik sleep: 15 dakika inaktiviteden sonra
- Cold start: ~30 saniye

**⚠️ Not:** Free plan'de service inaktif kalırsa uyur, ilk istek yavaş olabilir.

## 🔄 Güncelleme Workflow

```bash
# 1. Kod değişikliği yap
git add .
git commit -m "Feature: xyz"
git push origin main

# 2. Render otomatik deploy eder (2-5 dakika)
# 3. https://backend-duamiss.onrender.com health check yap
```

## 📞 Destek

- Render Docs: https://render.com/docs
- Django on Render: https://render.com/docs/deploy-django
- Community: https://community.render.com

---

**Son Güncelleme:** Ekim 2025
**Django Version:** 5.2.5
**Python Version:** 3.11.9
