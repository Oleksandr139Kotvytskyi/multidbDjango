"""
Django settings for MultiDatabaseDjango project.

Generated by 'django-admin startproject' using Django 4.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path

from db.src.db_managers.exasol_db_manager import ExasolDbManager
from db.src.db_managers.mysql_db_manager import MySQLDbManager
from db.src.db_managers.postgres_db_manager import PostgresDbManager
from db.src.factory.db_factory import DbConnectorFactory
import environ

from db.src.utils.utils import fill_cnf_file

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.str("DEBUG")

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'prototype',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'MultiDatabaseDjango.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'MultiDatabaseDjango.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
CORS_ORIGIN_ALLOW_ALL = True

# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO', }
}

# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

POSTGRES_CONFIG_FILE = BASE_DIR.joinpath('etc/db_conf/postgres.cnf')
EXASOL_CONFIG_FILE = BASE_DIR.joinpath('etc/db_conf/exasol.cnf')
MYSQL_CONFIG_FILE = BASE_DIR.joinpath('etc/db_conf/mysql.cnf')

fill_cnf_file(POSTGRES_CONFIG_FILE,
              env.str('DB_POSTGRES_DATABASE'),
              env.str('DB_POSTGRES_USER'),
              env.str('DB_POSTGRES_PASSWORD'),
              env.str('DB_POSTGRES_HOST'),
              env.str('DB_POSTGRES_PORT'),
              env.str('DB_POSTGRES_DELAY'),
              env.str('DB_POSTGRES_LIFETIME'),
              env.str('DB_POSTGRES_POOLSIZE'),
              )
fill_cnf_file(EXASOL_CONFIG_FILE,
              env.str('DB_EXASOL_DATABASE'),
              env.str('DB_EXASOL_USER'),
              env.str('DB_EXASOL_PASSWORD'),
              env.str('DB_EXASOL_HOST'),
              env.str('DB_EXASOL_PORT'),
              env.str('DB_EXASOL_DELAY'),
              env.str('DB_EXASOL_LIFETIME'),
              env.str('DB_EXASOL_POOLSIZE'),
              )
fill_cnf_file(MYSQL_CONFIG_FILE,
              env.str('DB_MYSQL_DATABASE'),
              env.str('DB_MYSQL_USER'),
              env.str('DB_MYSQL_PASSWORD'),
              env.str('DB_MYSQL_HOST'),
              env.str('DB_MYSQL_PORT'),
              env.str('DB_MYSQL_DELAY'),
              env.str('DB_MYSQL_LIFETIME'),
              env.str('DB_MYSQL_POOLSIZE'),
              )

database_connection_factory = DbConnectorFactory()

# database_connection_factory.register_manager(MySQLDbManager, MYSQL_CONFIG_FILE)
# database_connection_factory.register_manager(ExasolDbManager, EXASOL_CONFIG_FILE)
# database_connection_factory.register_manager(PostgresDbManager, POSTGRES_CONFIG_FILE)
