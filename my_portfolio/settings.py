"""
Django settings for my_portfolio project.
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# BASE DIRECTORY
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")


# ============================================================
# SECURITY
# ============================================================

SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-local-development-only",
)

DEBUG = os.environ.get("DJANGO_DEBUG", "0").lower() in {
    "1",
    "true",
    "yes",
}

ALLOWED_HOSTS = [
    host.strip()
    for host in os.environ.get(
        "DJANGO_ALLOWED_HOSTS",
        "127.0.0.1,localhost,.vercel.app",
    ).split(",")
    if host.strip()
]


# ============================================================
# APPLICATIONS
# ============================================================

INSTALLED_APPS = [
    "portfolio",
    "rest_framework",

    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
]


# ============================================================
# MIDDLEWARE
# ============================================================

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",

    # Serve static files in production
    "whitenoise.middleware.WhiteNoiseMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ============================================================
# URLS / TEMPLATES
# ============================================================

ROOT_URLCONF = "my_portfolio.urls"

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
                "portfolio.context_processors.profile_context",
            ],
        },
    },
]

WSGI_APPLICATION = "my_portfolio.wsgi.application"


# ============================================================
# DATABASE
# SQLITE ONLY
# ============================================================
if os.environ.get("VERCEL") or os.environ.get("NOW_REGION"):
    # Vercel's filesystem is read-only except for /tmp.
    sqlite_name = "/tmp/db.sqlite3"
else:
    # Local development
    sqlite_name = BASE_DIR / "db.sqlite3"
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": sqlite_name,
    }
}


# ============================================================
# PASSWORD VALIDATION
# ============================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# ============================================================
# INTERNATIONALIZATION
# ============================================================

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# ============================================================
# STATIC FILES
# ============================================================

STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "portfolio" / "static",
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": (
            "whitenoise.storage."
            "CompressedManifestStaticFilesStorage"
        ),
    },
}


# ============================================================
# MEDIA FILES
# ============================================================

MEDIA_URL = "/media/"

MEDIA_ROOT = BASE_DIR / "media"


# ============================================================
# PORTFOLIO CONFIGURATION
# ============================================================

PORTFOLIO_NAME = os.environ.get(
    "PORTFOLIO_NAME",
    "Samyog Panthee",
)

PORTFOLIO_EMAIL = os.environ.get(
    "PORTFOLIO_EMAIL",
    "samyogpanthee238@gmail.com",
)

PORTFOLIO_LINKEDIN = os.environ.get(
    "PORTFOLIO_LINKEDIN",
    "https://www.linkedin.com/in/samyog-panthee-87946442b/",
)

PORTFOLIO_GITHUB = os.environ.get(
    "PORTFOLIO_GITHUB",
    "https://github.com/samyog123-lang",
)

PORTFOLIO_INSTAGRAM = os.environ.get(
    "PORTFOLIO_INSTAGRAM",
    "https://www.instagram.com/samyogpanthee238/",
)

PORTFOLIO_FACEBOOK = os.environ.get(
    "PORTFOLIO_FACEBOOK",
    "https://www.facebook.com/samyogpanthee238",
)

PORTFOLIO_PHONE = os.environ.get(
    "PORTFOLIO_PHONE",
    "",
)

PORTFOLIO_LOCATION = os.environ.get(
    "PORTFOLIO_LOCATION",
    "Nepal",
)

PORTFOLIO_EDUCATION = os.environ.get(
    "PORTFOLIO_EDUCATION",
    "B.E. Information Technology Engineering",
)

PORTFOLIO_INSTITUTION = os.environ.get(
    "PORTFOLIO_INSTITUTION",
    "NCIT — Nepal College of Information Technology",
)

PORTFOLIO_RESUME = (
    BASE_DIR
    / "media"
    / "resume"
    / "samyog-panthee-resume.pdf"
)


# ============================================================
# OPENAI
# ============================================================

OPENAI_API_KEY = os.environ.get(
    "OPENAI_API_KEY",
    "",
)

OPENAI_MODEL = os.environ.get(
    "OPENAI_MODEL",
    "gpt-4.1-mini",
)


# ============================================================
# DJANGO REST FRAMEWORK
# ============================================================

REST_FRAMEWORK = {
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": 6,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
}


# ============================================================
# PRODUCTION SECURITY
# ============================================================

if not DEBUG:

    if SECRET_KEY == "django-insecure-local-development-only":
        raise ValueError(
            "Set DJANGO_SECRET_KEY for production."
        )

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_CONTENT_TYPE_NOSNIFF = True

    SECURE_HSTS_SECONDS = 31536000

    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

    SECURE_HSTS_PRELOAD = True


# ============================================================
# GENERAL DJANGO SETTINGS
# ============================================================

X_FRAME_OPTIONS = "DENY"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ============================================================
# EMAIL
# ============================================================

EMAIL_BACKEND = os.environ.get(
    "EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend",
)

EMAIL_HOST = os.environ.get(
    "EMAIL_HOST",
    "",
)

EMAIL_PORT = int(
    os.environ.get(
        "EMAIL_PORT",
        "587",
    )
)

EMAIL_USE_TLS = os.environ.get(
    "EMAIL_USE_TLS",
    "1",
).lower() in {
    "1",
    "true",
    "yes",
}

EMAIL_HOST_USER = os.environ.get(
    "EMAIL_HOST_USER",
    "",
)

EMAIL_HOST_PASSWORD = os.environ.get(
    "EMAIL_HOST_PASSWORD",
    "",
)

DEFAULT_FROM_EMAIL = os.environ.get(
    "DEFAULT_FROM_EMAIL",
    PORTFOLIO_EMAIL,
)