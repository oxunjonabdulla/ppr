from . import base

SECRET_KEY = base.env("SECRET_KEY")
ALLOWED_HOSTS = ["ppr.vchdqarshi.uz"]


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": base.env("POSTGRES_DB"),
        "USER": base.env("POSTGRES_USER"),
        "PASSWORD": base.env("POSTGRES_PASSWORD"),
        "HOST": base.env("POSTGRES_HOST", "db"),
        "PORT": "5432",
    }
}
