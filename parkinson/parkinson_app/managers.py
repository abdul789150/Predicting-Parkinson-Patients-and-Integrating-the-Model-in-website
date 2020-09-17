from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import ugettext_lazy
import random

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, full_name, gender, phone_number, **extra_fields):
        email = self.normalize_email(email)
        slug_name = full_name.replace(" ", "-")
        r_n = random.random()
        u_n = slug_name+str(r_n)
        user = self.model(email=email, full_name=full_name, username=u_n)
        user.slug_name = slug_name
        user.gender=gender
        user.phone_number=phone_number
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, full_name, gender, phone_number, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, full_name, gender, phone_number, **extra_fields)

    def add_new_user(self, email, **extra_fields):
        email = self.normalize_email(email)
        password = self.model.objects.make_random_password()
        user = self.model(email=email, password=password)
        # user.set_password(password)
        user.save()
        return user

    def create_new_superuser(self, email, **extra_fields):
        email = self.normalize_email(email)
        password = self.model.objects.make_random_password()
        user = self.model(email=email, password=password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save()
        return user