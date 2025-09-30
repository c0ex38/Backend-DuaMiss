from pathlib import Path
from datetime import timedelta
import environ

# Proje ana dizini
BASE_DIR = Path(__file__).resolve().parent.parent

# Ortam değişkenlerini yönetmek için environ ayarları
env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

# Django'nun güvenlik anahtarı
SECRET_KEY = env("SECRET_KEY", default="insecure-change-me")

# Geliştirme modu için True, prod için False olmalı
DEBUG = env.bool("DEBUG", default=False)

# Sunucunun cevap vereceği alan adları listesi
ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")]

# Projede yüklü olan uygulamalar
INSTALLED_APPS = [
    "django.contrib.admin",  # Django yönetim paneli
    "django.contrib.auth",  # Kimlik doğrulama sistemi
    "django.contrib.contenttypes",  # İçerik tipleri
    "django.contrib.sessions",  # Oturum yönetimi
    "django.contrib.messages",  # Mesaj frameworkü
    "django.contrib.staticfiles",  # Statik dosya yönetimi
    "rest_framework",  # Django REST framework
    "rest_framework_simplejwt",  # JWT tabanlı kimlik doğrulama
    "corsheaders",  # CORS yönetimi
    "users",  # Kullanıcı uygulaması
    "company",  # Şirket uygulaması
    "product",  # Ürün uygulaması
    "order",  # Sipariş uygulaması
]

# Django'da kullanılan middleware'ler (ara katman yazılımları)
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # CORS desteği
    "django.middleware.security.SecurityMiddleware",  # Güvenlik middleware'i
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Statik dosyaları servis etmek için
    "django.contrib.sessions.middleware.SessionMiddleware",  # Oturum yönetimi
    "django.middleware.common.CommonMiddleware",  # Ortak middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # CSRF koruması
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Kimlik doğrulama
    "django.contrib.messages.middleware.MessageMiddleware",  # Mesajlar
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Clickjacking koruması
]

# Ana URL yapılandırma dosyası
ROOT_URLCONF = "dashboard_project.urls"

# Şablon (template) ayarları
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Django template engine
        "DIRS": [],  # Ek şablon dizinleri
        "APP_DIRS": True,  # Uygulama içi şablonları kullan
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",  # Request nesnesini şablona ekler
                "django.contrib.auth.context_processors.auth",  # Kullanıcı nesnesini şablona ekler
                "django.contrib.messages.context_processors.messages",  # Mesajları şablona ekler
            ],
        },
    },
]

# WSGI uygulama yolu
WSGI_APPLICATION = "dashboard_project.wsgi.application"

# Veritabanı ayarları (PostgreSQL kullanılıyor)
# Öncelik: Direct (5432) URL; yoksa pooled (6543) URL'yi kullan.
_db_url_key = "DATABASE_URL_DIRECT" if env("DATABASE_URL_DIRECT", default=None) else "DATABASE_URL"
_db = env.db_url(_db_url_key)

_host = (_db.get("HOST") or "").lower()
_port = str(_db.get("PORT") or "")
_is_pooled = ("pooler" in _host) or (_port == "6543")  # Supabase PgBouncer (6543) ise True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": _db["NAME"],
        "USER": _db["USER"],
        "PASSWORD": _db["PASSWORD"],
        "HOST": _db["HOST"],
        "PORT": _db["PORT"],
        # PgBouncer (6543) ile daima 0; Direct (5432) ile bağlantıyı bir süre açık tut.
        "CONN_MAX_AGE": 0 if _is_pooled else 60,
        # Django 3.1+ bağlantı sağlık kontrolü
        "CONN_HEALTH_CHECKS": True,
        "OPTIONS": {
            "sslmode": "require",
            "connect_timeout": 5,
        },
    }
}

# PgBouncer ile server-side cursor'lar sorun çıkarabilir; pooled'da kapatıyoruz.
if _is_pooled:
    DATABASES["default"]["DISABLE_SERVER_SIDE_CURSORS"] = True

# Şifre doğrulama kuralları
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},  # Kullanıcıya benzer şifre engeli
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},  # Minimum uzunluk kontrolü
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},  # Yaygın şifre engeli
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},  # Tamamen sayısal şifre engeli
]

# Dil ve zaman ayarları (Türkiye için)
LANGUAGE_CODE = "tr-tr"  # Varsayılan dil kodu
TIME_ZONE = "Europe/Istanbul"  # Zaman dilimi
USE_I18N = True  # Uluslararasılaştırma desteği
USE_TZ = True  # Zaman dilimi kullanımı

# Statik dosya URL ve kök dizini
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Varsayılan otomatik alan tipi (büyük tamsayı)
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework ayarları
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # JWT ile kimlik doğrulama
    ),
}

# JWT (JSON Web Token) ayarları
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),  # Erişim token'ı ömrü (prod için öneri)
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Yenileme token'ı ömrü
    "ROTATE_REFRESH_TOKENS": True,  # Yenileme token'ı döndürülünce yenisini üret
    "BLACKLIST_AFTER_ROTATION": True,  # Dönen token'ı kara listeye al
    "UPDATE_LAST_LOGIN": True,  # Son giriş tarihini güncelle
}

# CORS (Cross-Origin Resource Sharing) ayarları
CORS_ALLOW_ALL_ORIGINS = False  # Tüm kaynaklara izin verme
CORS_ALLOWED_ORIGINS = [o.strip() for o in env("CORS_ALLOWED_ORIGINS", default="http://localhost:3000").split(",")]  # İzin verilen origin listesi

# Varsayılan kullanıcı modeli
AUTH_USER_MODEL = "users.CustomUser"

# Statik dosyalar için WhiteNoise ayarı
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Proxy arkasında HTTPS algılaması için ayar
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
