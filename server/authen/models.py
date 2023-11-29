from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_files):
        if not email:
            raise ValueError(_("The Email field must be set!"))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_files)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_files):
        extra_files.setdefault("is_staff", True)
        extra_files.setdefault("is_superuser", True)

        if extra_files.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))

        if extra_files.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_files)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=30)
    email = models.EmailField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self) -> str:
        return f"{ self.username } : { self.email }"
