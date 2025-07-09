from . import base
from .base import *  # noqa: F403

DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": base.env.str("POSTGRES_DB"),
        "USER": base.env.str("POSTGRES_USER"),
        "PASSWORD": base.env.str("POSTGRES_PASSWORD"),
        "HOST": base.env.str("POSTGRES_HOST", default="db"),
        "PORT": "5432",
    }
}
