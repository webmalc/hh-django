DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'hh',
        'USER': 'postgres',
        'PASSWORD': 'qwerty',
        'HOST': '127.0.0.1',
        'PORT': '5432'
    }
}

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'webmalc'
EMAIL_HOST_PASSWORD = 'irlebaslfkwcjyva'

ADMINS = (('Sergey', 'webmalc@gmail.com'),)

SECRET_KEY = '123dsaasdaw123dasd23134123'
ALLOWED_HOSTS = ['*']
DEBUG = True

