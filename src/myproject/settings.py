import os
from secret_gen import get_secret, generate_random_string
from config_mgmt import config_gen


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_NAME = os.path.split(BASE_DIR)[-1]

""" Try to get the settings config from the environment variable
    'DJANGO_PROJECT_CONF_LOCATION'.
    If the variable doesnt exist, try to check/create a directory
    with the project name in /etc and save the settings there.
"""
CONF_LOCATION = os.environ.get('DJANGO_PROJECT_CONF_LOCATION')
if CONF_LOCATION is None:
    if not os.path.exists("/etc/{}".format(PROJECT_NAME)):
        os.mkdir("/etc/{}".format(PROJECT_NAME))
    CONF_LOCATION = "/etc/{}/settings.conf".format(PROJECT_NAME)

EXAMPLE_CONF_LOCATION = os.path.join(BASE_DIR, "{}/settings.conf.example".format(PROJECT_NAME))

try:
    VERSION = open(os.path.join(BASE_DIR, 'VERSION.txt')).read()
except Exception as e:
    VERSION = 'ERROR: {}'.format(str(e))

CONFIG = config_gen(CONF_LOCATION, EXAMPLE_CONF_LOCATION)

""" SECURITY WARNING: keep the secret key used in production secret!
    Check for a config value for secret_location for a file containing
    a secret.  If the setting is not present, check for a setting
    for secret.  Otherwise, generate a secret and save it to the
    config file.
"""
if CONFIG.has_option('django', 'secret_location'):
    SECRET_LOCATION = CONFIG.get('django', 'secret_location')
    SECRET_KEY = get_secret(SECRET_LOCATION)
elif CONFIG.has_option('django', 'secret'):
    SECRET_KEY = CONFIG.get('django', 'secret')
else:
    SECRET_KEY = generate_random_string()
    CONFIG.set('django', 'secret', SECRET_KEY)
    with open(CONF_LOCATION, 'w') as fh:
        CONFIG.write(fh)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = CONFIG.getboolean('django', 'debug')

ALLOWED_HOSTS = CONFIG.get('django', 'allowed_hosts').split(',')

ADMINS = CONFIG.get('django', 'admins')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

INSTALLED_APPS.extend(CONFIG.get('django', 'apps').split(','))

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '{}.urls'.format(PROJECT_NAME)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', '{0}/../../templates'.format(BASE_DIR)],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': CONFIG.getboolean('django', 'template_debug'),  # enable template debug
        },
    },
]

WSGI_APPLICATION = '{}.wsgi.application'.format(PROJECT_NAME)


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {}

if CONFIG.get('database:default', 'db_backend') == 'sqlite3':
    if CONFIG.has_option('database:default', 'sqlite3_location'):
        sqlite3_location = CONFIG.get('database:default', 'sqlite3_location')
    else:
        sqlite3_location = os.path.join(BASE_DIR, 'db.sqlite3')
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': sqlite3_location,
    }
else:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': CONFIG.get('database:default', 'db_name'),
        'USER': CONFIG.get('database:default', 'db_user'),
        'PASSWORD': CONFIG.get('database:default', 'db_pass'),
        'HOST': CONFIG.get('database:default', 'db_host'),
    }

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
NOSE_ARGS = [
    '--with-xunit',
    '--xunit-file=/tmp/tests/results/results.xml',
] 

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = CONFIG.get('django', 'language_code')

TIME_ZONE = CONFIG.get('django', 'timezone')

USE_I18N = CONFIG.getboolean('django', 'use_i18n')

USE_L10N = CONFIG.getboolean('django', 'use_l10n')

USE_TZ = CONFIG.getboolean('django', 'use_tz')

LOG_FILE = CONFIG.get('django', 'log_file')

SQL_LOG_FILE = CONFIG.get('debugging', 'sql_log_file')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'simple': {
            'format': '[%(asctime)s] %(levelname)-8s"%(message)s"'
        },
    },
    'handlers': {
        'file': {
            'level': CONFIG.get('django', 'log_level'),
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'simple',
        },
        'sqldb_file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': SQL_LOG_FILE,
            'formatter': 'simple',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'loggers': {
        'debug': {
            'handlers': ['file'],
            'level': CONFIG.get('django', 'log_level'),
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['null'],  # Quiet by default!
            'propagate': False,
            'level':'DEBUG',
        },
    },
}
if CONFIG.getboolean('debugging', 'sql_logging'):
    LOGGING['loggers']['django.db.backends']['handlers'] = ['sqldb_file']


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_ROOT = CONFIG.get('django', 'static_root')
STATIC_URL = CONFIG.get('django', 'static_url')
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
    os.path.join(BASE_DIR, "templates"),
)

LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = "/"
LOGIN_URL = "/login/"
