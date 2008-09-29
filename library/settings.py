import os, platform

DEVELOPMENT_MODE = (platform.node() != 'nas')

ADMINS = (
    ('Arnaud Rebts', 'arnaud.rebts@gmail.com'),
)

MANAGERS = ADMINS

if DEVELOPMENT_MODE:
    DEBUG = True
    DATABASE_ENGINE = 'sqlite3'
    DATABASE_NAME = 'dev.sqlite3'
    LIBRARY_ROOT = '/Users/kid/Movies/'
else:
    DEBUG = False
    DATABASE_ENGINE = 'postgresql_psycopg2'
    DATABASE_NAME = 'new-library'
    DATABASE_USER = 'django'
    DATABASE_PASSWORD = ''
    DATABASE_HOST = '127.0.0.1'
    DATABASE_PORT = '5678'
    LIBRARY_ROOT = '/data/Library/'
TEMPLATE_DEBUG = DEBUG

TIME_ZONE = 'Europe/Brussels'

LANGUAGE_CODE = 'fr-be'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/admin/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'jagz76z&zffejk(+hdbmn*9!f6a59-7_q97zsadzm3z_qo*t&z'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.middleware.transaction.TransactionMiddleware',
)

ROOT_URLCONF = 'library.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'common',
    'series',
)