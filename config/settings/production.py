import requests
from dj_database_url import parse as db_url

from .base import *
from .base import env

# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = env('SECRET_KEY')
# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALLOWED_HOSTS = env('ALLOWED_HOSTS', default=['example.com'], cast=list)
ALLOWED_HOSTS = ['api.regis-blog-me.com']
try:
    EC2_IP = requests.get('http://169.254.169.254/latest/meta-data/local-ipv4').text
    ALLOWED_HOSTS.append(EC2_IP)
except requests.exceptions.RequestException:
    pass

CORS_ORIGIN_WHITELIST = (
    'https://regis-blog-me.com',
)

# DATABASES
# ------------------------------------------------------------------------------
DATABASES = {
    'default': env('DATABASE_URL', cast=db_url)
}
DATABASES['default']['ATOMIC_REQUESTS'] = True
DATABASES['default']['CONN_MAX_AGE'] = env('CONN_MAX_AGE', default=60, cast=int)

# SECURITY
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-proxy-ssl-header
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-ssl-redirect
SECURE_SSL_REDIRECT = env('SECURE_SSL_REDIRECT', default=True, cast=bool)

# https://docs.djangoproject.com/en/dev/ref/settings/#session-cookie-secure
SESSION_COOKIE_SECURE = True

# SESSION_COOKIE_HTTPONLY = True

# https://docs.djangoproject.com/en/dev/ref/settings/#csrf-cookie-secure
CSRF_COOKIE_SECURE = True

# CSRF_COOKIE_HTTPONLY = True

X_FRAME_OPTIONS = 'SAMEORIGIN'

# https://docs.djangoproject.com/en/dev/topics/security/#ssl-https
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-seconds
# TODO: set this to 60 seconds first and then to 518400 once you prove the former works
SECURE_HSTS_SECONDS = 60

# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-include-subdomains
SECURE_HSTS_INCLUDE_SUBDOMAINS = env(
    'SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool
)
# https://docs.djangoproject.com/en/dev/ref/settings/#secure-hsts-preload
SECURE_HSTS_PRELOAD = env('SECURE_HSTS_PRELOAD', default=True, cast=bool)

# https://docs.djangoproject.com/en/dev/ref/middleware/#x-content-type-options-nosniff
SECURE_CONTENT_TYPE_NOSNIFF = env(
    'SECURE_CONTENT_TYPE_NOSNIFF', default=True, cast=bool
)

# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env('ADMIN_URL', default='admin/')


# STORAGE CONFIGURATION
# ------------------------------------------------------------------------------
# Uploaded Media Files
# ------------------------
# See: http://django-storages.readthedocs.io/en/latest/index.html
INSTALLED_APPS += ['storages', ]

AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME')
AWS_AUTO_CREATE_BUCKET = True
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = True
AWS_S3_SIGNATURE_VERSION = 's3v4'
AWS_S3_REGION_NAME = 'us-east-1'

# AWS cache settings, don't change unless you know what you're doing:
AWS_EXPIRY = 60 * 60 * 24 * 7

# TODO See: https://github.com/jschneier/django-storages/issues/47
# Revert the following and use str after the above-mentioned bug is fixed in
# either django-storage-redux or boto
control = 'max-age=%d, s-maxage=%d, must-revalidate' % (AWS_EXPIRY, AWS_EXPIRY)
AWS_HEADERS = {
    'Cache-Control': bytes(control, encoding='latin-1')
}

# URL that handles the media served from MEDIA_ROOT, used for managing
# stored files.
MEDIA_URL = 'https://s3.amazonaws.com/%s/' % AWS_STORAGE_BUCKET_NAME
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp-relay.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Sentry Configuration
# TODO: Update the env variable for DJANGO_SENTRY_DSN for production
SENTRY_DSN = env('DJANGO_SENTRY_DSN',
                 default='https://83ba5579ad964d78947490b8f007d8c5@o859262.ingest.sentry.io/6302874')
if SENTRY_DSN:
    import sentry_sdk
    from sentry_sdk.integrations.django import DjangoIntegration
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        send_default_pii=True
    )
