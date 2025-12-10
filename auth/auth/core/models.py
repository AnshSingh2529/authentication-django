from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)

# Create your models here.


class CustomerUserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True")

        return self.create_user(username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30, blank=False, null=False)
    last_name = models.CharField(max_length=30, blank=False, null=False)
    username = models.CharField(
        max_length=150,
        unique=True,
        blank=False,
        null=False,
        help_text="Unique username for the user.",
    )
    contact_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        help_text="Optional contact number of the user.",
        unique=True,
    )
    password = models.CharField(
        max_length=128,
        blank=False,
        null=False,
        help_text="Password for the user account.",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Designates whether this user should be treated as active.",
    )
    last_login = models.DateTimeField(
        blank=True,
        null=True,
        help_text="The last time the user logged in.",
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the user account was created.",
    )

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    objects = CustomerUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["contact_number", "password"]

    def __str__(self):
        return f"{self.username} - ({self.first_name} {self.last_name} -- {self.contact_number})"
