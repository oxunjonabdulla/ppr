from . import base

DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": base.env("POSTGRES_DB"),
        "USER": base.env("POSTGRES_USER"),
        "PASSWORD": base.env("POSTGRES_PASSWORD"),
        "HOST": base.env("POSTGRES_HOST"),
        "PORT": "5432",
    }
}
