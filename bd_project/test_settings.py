"""
Testovací nastavení – používá SQLite místo PostgreSQL.

POZNÁMKA: Testy jsou určeny ke spuštění v Dockeru (Python 3.12 + Django 5.2).
Lokálně jsou podmíněně spustitelné jen model/URL/admin testy.

Spuštění v Dockeru (doporučeno):
    docker compose exec web python manage.py test

Lokálně (pouze bez renderování šablon – Python 3.14 + Django 5.2 nutné):
    python manage.py test --settings=bd_project.test_settings
"""
from .settings import *  # noqa: F401, F403

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Vypnout Whitenoise – v testech nepotřebujeme statické soubory
MIDDLEWARE = [m for m in MIDDLEWARE if 'whitenoise' not in m.lower()]  # noqa: F405
INSTALLED_APPS = [a for a in INSTALLED_APPS if a != 'whitenoise.runserver_nostatic']  # noqa: F405
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# Rychlejší hašování hesel v testech
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]
