import io
import os
from urllib.parse import urlparse

import environ
import google.auth
from google.cloud import secretmanager

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# [START cloudrun_django_secret_config]
# SECURITY WARNING: don't run with debug turned on in production!
# Change this to "False" when you are ready for production
env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")

try:
    _, os.environ["GOOGLE_CLOUD_PROJECT"] = google.auth.default()

except google.auth.exceptions.DefaultCredentialsError:
    pass

if os.path.isfile(env_file):
    # Use a local secret file, if provided
    env.read_env(env_file)

elif os.getenv("TRAMPOLINE_CI", None):
    # Create local settings if running with CI, for unit testing

    placeholder = (
        f"SECRET_KEY=a\n"
        "GS_BUCKET_NAME=None\n"
        f"DATABASE_URL=sqlite://{os.path.join(BASE_DIR, 'db.sqlite3')}"
    )
    env.read_env(io.StringIO(placeholder))
# [END_EXCLUDE]
elif os.environ.get("GOOGLE_CLOUD_PROJECT", None):
    # Pull secrets from Secret Manager
    project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    client = secretmanager.SecretManagerServiceClient()
    settings_name = os.environ.get("SETTINGS_NAME", "turage-settings") # TODO: add on .env
    name = f"projects/{project_id}/secrets/{settings_name}/versions/latest"
    payload = client.access_secret_version(name=name).payload.data.decode("UTF-8")

    env.read_env(io.StringIO(payload))
else:
    raise Exception("No local .env or GOOGLE_CLOUD_PROJECT detected. No secrets found.")
# [END cloudrun_django_secret_config]
SECRET_KEY = env("SECRET_KEY")

DEBUG = env("DEBUG")

# [START cloudrun_django_csrf]
# SECURITY WARNING: It's recommended that you use this when
# running in production. The URL will be known once you first deploy
# to Cloud Run. This code takes the URL and converts it to both these settings formats.
CLOUDRUN_SERVICE_URL = env("CLOUDRUN_SERVICE_URL", default=None)
if CLOUDRUN_SERVICE_URL:
    ALLOWED_HOSTS = [urlparse(CLOUDRUN_SERVICE_URL).netloc]
    CSRF_TRUSTED_ORIGINS = [CLOUDRUN_SERVICE_URL]
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
else:
    ALLOWED_HOSTS = ["*"]
# [END cloudrun_django_csrf]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "widget_tweaks",
    "storages",
    "turage",
    "accounts",
    "ride",

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "turage.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
WSGI_APPLICATION = "turage.wsgi.application"

# Database
# [START cloudrun_django_database_config]
# Use django-environ to parse the connection string

if os.getenv("USE_LOCAL_DB"):

    DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR + '/db.sqlite3',
        }
    }



else:
    # connect to postgresql database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': 'turage',
            'USER': os.getenv('DB_USER'),
            'PASSWORD': os.getenv('DB_PASSWORD'),
            'HOST': os.getenv('DB_HOST'),
            'PORT': 5432,
        }}
print(DATABASES) 
# If the flag as been set, configure to use proxy
# if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
#     DATABASES["default"]["HOST"] = "127.0.0.1"
#     DATABASES["default"]["PORT"] = 5400


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

AUTH_USER_MODEL = 'ride.TurageUser'

# Static files (CSS, JavaScript, Images)
# [START cloudrun_django_static_config]
# Define static storage via django-storages[google]

if os.getenv("GS_BUCKET_NAME", None) == None:
    STATIC_URL = "/static/"
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    DEFAULT_FILE_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
    STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"
else:
    GS_BUCKET_NAME = env("GS_BUCKET_NAME")
    STATIC_URL = "/static/"
    DEFAULT_FILE_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    STATICFILES_STORAGE = "storages.backends.gcloud.GoogleCloudStorage"
    GS_DEFAULT_ACL = "publicRead"
# [END cloudrun_django_static_config]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

EMAIL_BACKEND = 'django_ses.SESBackend'

AWS_SES_REGION_ENDPOINT = "email.us-east-1.amazonaws.com"

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID", None)
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY", None)
AWS_SES_REGION_NAME = os.environ.get("AWS_SES_REGION_NAME", None)

OPENROUTE_API_KEY = os.environ.get("OPENROUTE_API_KEY", None)

EMAIL_ENABLED = os.environ.get("EMAIL_ENABLED", None)