"""
Django settings for PasswordManager project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-979tio4-^#s7v&x=%*k=l12um-1hruzhc9rm4&-gc$%v(&03(3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'password_manager_app',
    'crispy_forms',
    'crispy_bootstrap5',
    'encrypted_model_fields',
    'fontawesomefree',
    'bootstrapform',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'PasswordManager.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'PasswordManager/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'PasswordManager.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases


PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    'django.contrib.auth.hashers.SHA1PasswordHasher',
    'django.contrib.auth.hashers.MD5PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedSHA1PasswordHasher',
    'django.contrib.auth.hashers.UnsaltedMD5PasswordHasher',
    'django.contrib.auth.hashers.CryptPasswordHasher',
]

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.MyMinimumLengthValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.UpperCaseCharacterValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.LowerCaseCharacterValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.DigitsCharacterValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.SymbolCharacterValidator',
    },
    {
        'NAME': 'PasswordManager.PasswordHelper.password_validator.MyUserAttributeSimilarityValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
AUTH_USER_MODEL = 'password_manager_app.User'

LOGIN_REDIRECT_URL = '/home'
LOGOUT_REDIRECT_URL = '/login'
LOGIN_URL = 'login'

try:
    from PasswordManager.localsettings import DATABASES
except ModuleNotFoundError:
    print("No database configuration in localsettings.py!")
    print("Complete the data and try again")
    exit(0)

try:
    from PasswordManager.localsettings import FIELD_ENCRYPTION_KEY
except ModuleNotFoundError:
    print("No module FIELD_ENCRYPTION_KEY in localsettings.py")
    exit(0)

try:
    from PasswordManager.localsettings import EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_USE_TLS, EMAIL_HOST_USER, \
        EMAIL_HOST_PASSWORD
except ModuleNotFoundError:
    print("No module email in localsettings.py")
    exit(0)
