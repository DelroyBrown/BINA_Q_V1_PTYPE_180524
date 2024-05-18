from django.db import models
import random
import string
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    bina_q_id = models.CharField(max_length=50, unique=True, blank=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_temporary_password = models.BooleanField(default=True)

    objects = UserManager()

    USERNAME_FIELD = "bina_q_id"
    REQUIRED_FIELDS = ["first_name", "last_name", "email"]

    def save(self, *args, **kwargs):
        if not self.bina_q_id:
            self.bina_q_id = self.generate_bina_q_id()
        super(User, self).save(*args, **kwargs)

    def generate_bina_q_id(self):
        first_three_first_name = self.first_name[:3].upper()
        first_three_last_name = self.last_name[:3].upper()
        random_chars = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        return f"{first_three_first_name}{first_three_last_name}-{random_chars}"

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"
