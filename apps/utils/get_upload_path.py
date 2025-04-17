import os
from datetime import date


def get_upload_path(instance, filename):
    today = date.today().strftime("%Y-%m-%d")

    model_name = instance.__class__.__name__
    if model_name == "User":
        folder_name = "users/profile"
        number = instance.username
    else:
        folder_name = "uploads"
        number = "unknown"
    return os.path.join(folder_name, today, str(number), filename)
