from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class JSHSHIRBackend(ModelBackend):
    def authenticate(
            self, request, username=None, jshshir=None, password=None, **kwargs
    ):
        if jshshir is None or password is None:
            return None

        try:
            user = User.objects.get(jshshir=jshshir)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
            return None

        if username is not None:
            try:
                user = User.objects.get(username=username)
                if user.check_password(password):
                    return user
            except User.DoesNotExist:
                return None
