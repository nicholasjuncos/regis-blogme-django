from .base import *
from dj_database_url import parse as db_url

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG

SECRET_KEY = env('SECRET_KEY', default='6%y2#3a(u%_7*b@y@4ei$z^jn+k^b1+m67o+h9sg_@r*ibl#+j')

# mailhog config
EMAIL_PORT = 1025

EMAIL_HOST = 'localhost'

# Cors Headers setup (May not be needed for this project)
# ------------------------------------------------------------------------------
# MIDDLEWARE = ['corsheaders.middleware.CorsMiddleware', ] + MIDDLEWARE
# INSTALLED_APPS += [ 'corsheaders', ]

INTERNAL_IPS = ['127.0.0.1', ]

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

########## CELERY
# In development, all tasks will be executed locally by blocking until the task returns
# CELERY_ALWAYS_EAGER = True
########## END CELERY

# ALLOWED_HOSTS CONFIG
ALLOWED_HOSTS = [
    '0.0.0.0',
    'localhost',
    '127.0.0.1',
]

# DATABASE CONFIG
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# https://pypi.org/project/python-decouple/#example-how-do-i-use-it-with-django
DATABASES = {
    'default': env('DATABASE_URL', default='sqlite:///' + str(BASE_DIR / 'db.sqlite3'), cast=db_url)
}

CORS_ORIGIN_ALLOW_ALL = True

# May not bee needed for this project
# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:4200',
#     'http://localhost:8080',
# ]

# REDIS_ENDPOINT_ADDRESS = env('REDIS_ENDPOINT_ADDRESS', default='localhost')
# REDIS_PORT = env('REDIS_PORT', '6379')
# REDIS_LOCATION = 'redis://{}:{}/1'.format(
#     REDIS_ENDPOINT_ADDRESS,
#     REDIS_PORT
# )
#
# # If select2 redis instance is same as normal redis, then redis instance will separate select2's cache
# SELECT2_REDIS_ENDPOINT_ADDRESS = env('SELECT2_REDIS_ENDPOINT_ADDRESS', default=REDIS_ENDPOINT_ADDRESS)
# if SELECT2_REDIS_ENDPOINT_ADDRESS == REDIS_ENDPOINT_ADDRESS:
#     SELECT2_REDIS_NUMBER = '2'
# else:
#     SELECT2_REDIS_NUMBER = '1'
#
# SELECT2_REDIS_LOCATION = 'redis://{}:{}/{}'.format(
#     SELECT2_REDIS_ENDPOINT_ADDRESS,
#     env('SELECT2_REDIS_PORT', default=REDIS_PORT),
#     SELECT2_REDIS_NUMBER
# )
#
#
# # If celery redis instance is same as normal redis, then redis instance will separate celery's cache
# CELERY_REDIS_ENDPOINT_ADDRESS = env('CELERY_REDIS_ENDPOINT_ADDRESS', default=REDIS_ENDPOINT_ADDRESS)
# if CELERY_REDIS_ENDPOINT_ADDRESS == REDIS_ENDPOINT_ADDRESS:
#     CELERY_REDIS_NUMBER = '3'
# else:
#     CELERY_REDIS_NUMBER = '1'
#
# CELERY_REDIS_LOCATION = 'redis://{}:{}/{}'.format(
#     CELERY_REDIS_ENDPOINT_ADDRESS,
#     env('CELERY_REDIS_PORT', default=REDIS_PORT),
#     CELERY_REDIS_NUMBER
# )
#
# CACHES = {
#     'default': {
#         'BACKEND': 'django_redis.cache.RedisCache',
#         'LOCATION': REDIS_LOCATION,
#         'OPTIONS': {
#             'CLIENT_CLASS': 'django_redis.client.DefaultClient',
#             'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
#             # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         }
#         # 'TIMEOUT': 900
#     },
#     'select2': {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": SELECT2_REDIS_LOCATION,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             'IGNORE_EXCEPTIONS': True,  # mimics memcache behavior.
#             # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         },
#         'TIMEOUT': 60 * 60 * 24,  # None
#     },
#     'celery': {
#         "BACKEND": "django_redis.cache.RedisCache",
#         "LOCATION": CELERY_REDIS_LOCATION,
#         "OPTIONS": {
#             "CLIENT_CLASS": "django_redis.client.DefaultClient",
#             'IGNORE_EXCEPTION': True,  # mimics memcache behavior.
#             # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
#         }
#     }
# }
#
# SELECT2_CACHE_BACKEND = 'select2'

# INSTALLED_APPS += ['storages', ]

# AWS_ACCESS_KEY_ID = env('DJANGO_AWS_ACCESS_KEY_ID', default='')
# AWS_SECRET_ACCESS_KEY = env('DJANGO_AWS_SECRET_ACCESS_KEY', default='')
# AWS_STORAGE_BUCKET_NAME = env('DJANGO_AWS_STORAGE_BUCKET_NAME', default='')
# AWS_AUTO_CREATE_BUCKET = True
# AWS_QUERYSTRING_AUTH = False
# AWS_S3_FILE_OVERWRITE = True
# AWS_S3_SIGNATURE_VERSION = 's3v4'
# AWS_S3_REGION_NAME = 'us-east-2'

