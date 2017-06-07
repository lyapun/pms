from .settings import *  # noqa

INSTALLED_APPS.append('test_without_migrations')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
