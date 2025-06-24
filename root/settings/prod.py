from . import base
from .base import *  # noqa: F403

SECRET_KEY = base.env("SECRET_KEY")
# ALLOWED_HOSTS = ["ppr.vchdqarshi.uz"]
ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "85.190.243.196",
    "ppr.vchdqarshi.uz",
    "api.ppr.vchdqarshi.uz",
]


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
