import os
from dotenv import load_dotenv
from os.path import join, dirname
import dj_database_url

# Needed to import API authentication codes from .env in root directory.
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# Redirect URLs for authentication
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# DEVELOPMENT SETTINGS
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '!(q6v&qi3-w-ktcqx_vaf6b4*#lh46u07+6+-41$0vqc9y$#$e'
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
ALLOWED_HOSTS = ['http', 'https', 'sounds.arts.uwa.edu.au',
                 '130.95.5.104', 'localhost', '127.0.0.1', '[::1]', '10.20.237.178', 'museum-of-sound.herokuapp.com']


# Application definition
INSTALLED_APPS = [
    'crispy_forms',
    'frontend',
    'users',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'storages',
    # 'django.contrib.gis',
    'whitenoise.runserver_nostatic'
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'adminportal.urls'

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
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'adminportal.wsgi.application'

# Database definition
''' 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': 'localhost',
        'NAME': 'mosdb',
        'PASSWORD': 'password',
        'USER': 'admin',
    }
}
'''
DATABASES = {}
DATABASES['default'] = dj_database_url.config(conn_max_age=600)
#'''

# Password validation

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

# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# MEDIA_URL = '/mediafiles/'
# MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

CRISPY_TEMPLATE_PACK = 'bootstrap4'
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': ('%(asctime)s [%(process)d] [%(levelname)s] ' +
                       'pathname=%(pathname)s lineno=%(lineno)s ' +
                       'funcname=%(funcName)s %(message)s'),
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        }
    },
    'handlers': {
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'testlogger': {
            'handlers': ['console'],
            'level': 'INFO',
        }
    }
}
DEBUG_PROPAGATE_EXCEPTIONS = True
LOGIN_URL = 'login'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

ADMIN_MEDIA_PREFIX = ''
SOUND_DIR = 'sounds/'
PROD_DIR = 'productions/'

