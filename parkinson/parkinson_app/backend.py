from django.conf import settings
from django.contrib.auth.hashers import check_password
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomBackend(BaseBackend):
    def authenticate_with_email(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email)
            if check_password(password, user.password):
                return user
        except User.DoesNotExist:
            return None