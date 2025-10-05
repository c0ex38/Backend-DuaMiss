# 🔧 Supabase Connection Fix

## Sorun
Render'da Supabase'e bağlanırken:
```
connection to server at "aws-1-eu-central-1.pooler.supabase.com" port 5432 failed: Connection refused
```

## Neden
- Supabase'in **Transaction mode** (port 5432) Django ile uyumlu değil
- **Session mode** (port 6543) kullanılmalı

## Çözüm

### 1. Supabase Dashboard'dan Doğru Connection String Al

1. [Supabase Dashboard](https://supabase.com/dashboard) → Your Project
2. **Settings** → **Database**
3. **Connection Pooling** sekmesi
4. **Session mode** seç
5. Connection string'i kopyala:

```bash
postgresql://postgres.xxxxx:[YOUR-PASSWORD]@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

⚠️ **DİKKAT:** Port **6543** olmalı (5432 değil!)

### 2. Render Environment'a Ekle

1. Render Dashboard → Your Service → **Environment**
2. `DATABASE_URL` değişkenini bul
3. Değerini değiştir:

```bash
# ESKİ (YANLIŞ - port 5432):
postgresql://postgres.xxxxx:password@aws-1-eu-central-1.pooler.supabase.com:5432/postgres

# YENİ (DOĞRU - port 6543):
postgresql://postgres.xxxxx:password@aws-1-eu-central-1.pooler.supabase.com:6543/postgres
```

4. **Save Changes**
5. **Manual Deploy** → Deploy latest commit

### 3. settings.py Güncellemesi (Opsiyonel)

Supabase Session mode için önerilen ayarlar:

```python
# PostgreSQL için özel ayarlar
if DATABASES["default"]["ENGINE"] == "django.db.backends.postgresql":
    DATABASES["default"]["CONN_MAX_AGE"] = 60  # Session mode için bağlantı havuzu
    DATABASES["default"]["OPTIONS"] = {
        "sslmode": "require",
        "connect_timeout": 10,
    }
```

## Alternatif: Render PostgreSQL Kullan (ÖNERİLEN)

Supabase yerine Render'ın kendi PostgreSQL'ini kullanmak daha kolay:

1. **Render Dashboard → New + → PostgreSQL**
   - Name: `duamiss-db`
   - Free plan seç
   - Create

2. **Web Service → Environment**
   - Mevcut `DATABASE_URL`'i sil
   - Render otomatik bağlayacak (`render.yaml` sayesinde)

3. **Redeploy**

## Test

```bash
# Connection test
curl https://backend-duamiss.onrender.com/api/

# Token test
curl -X POST https://backend-duamiss.onrender.com/api/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123456"}'
```

## Render Shell'den Debug

```bash
# Render Dashboard → Shell
python manage.py check --database default
python manage.py migrate
python manage.py createsuperuser
```

---

**Öneri:** Free tier için Render PostgreSQL daha stabil ve kolay. Supabase production'da kullanmak istiyorsan mutlaka Session mode + port 6543 kullan!
