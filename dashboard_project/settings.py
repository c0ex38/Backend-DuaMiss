from pathlib import Path
from datetime import timedelta
import environ

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    DEBUG=(bool, False),
)
environ.Env.read_env(BASE_DIR / ".env")

SECRET_KEY = env("SECRET_KEY", default="insecure-change-me")
DEBUG = env.bool("DEBUG", default=False)

ALLOWED_HOSTS = [h.strip() for h in env("ALLOWED_HOSTS", default="localhost,127.0.0.1").split(",")]

# --- Frontend / CORS / CSRF ---
# Comma-separated full origins, e.g. "https://your-frontend.vercel.app,https://www.yourdomain.com"
FRONTEND_ORIGINS = [o.strip() for o in env("FRONTEND_ORIGINS", default="").split(",") if o.strip()]

# If you prefer to allow all during early staging, keep CORS_ALLOW_ALL_ORIGINS=True below.
# For production, explicitly set allowed origins via FRONTEND_ORIGINS.
CORS_ALLOWED_ORIGINS = FRONTEND_ORIGINS

# CSRF requires scheme in Django 4+ (e.g., "https://example.com")
CSRF_TRUSTED_ORIGINS = FRONTEND_ORIGINS

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "users",
    "company",
    "product",
    "order",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "dashboard_project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "dashboard_project.wsgi.application"

DATABASES = {
    "default": (
        # Prefer DATABASE_URL if provided (Railway, Render, etc.)
        env.db_url("DATABASE_URL", default=None)
        and {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env.db_url("DATABASE_URL")["NAME"],
            "USER": env.db_url("DATABASE_URL")["USER"],
            "PASSWORD": env.db_url("DATABASE_URL")["PASSWORD"],
            "HOST": env.db_url("DATABASE_URL")["HOST"],
            "PORT": env.db_url("DATABASE_URL")["PORT"],
            "CONN_MAX_AGE": 0,
            "OPTIONS": {
                # Railway supports TLS; if your instance doesn't, override via env: PGSSLMODE=disable
                "sslmode": env("PGSSLMODE", default="require"),
                "connect_timeout": 10,
            },
        }
    ) or {
        # Local fallback (no DATABASE_URL): use SQLite
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "tr-tr"
TIME_ZONE = "Europe/Istanbul"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
}

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

AUTH_USER_MODEL = "users.CustomUser"

STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# --- Security (production) ---
USE_X_FORWARDED_HOST = True

if not DEBUG:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 60 * 60 * 24  # 1 day to start; increase after confirming HTTPS works
    SECURE_HSTS_INCLUDE_SUBDOMAINS = False
    SECURE_HSTS_PRELOAD = False
    SECURE_SSL_REDIRECT = True
