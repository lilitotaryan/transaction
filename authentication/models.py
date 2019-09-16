from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


class VivaroUserManager(models.Manager):
    _password = None

    def _set_password(self, password):
        _password = make_password(password)

    def _create_user(self, username, phone_number, password, email, **other):
        if not phone_number:
            raise ValueError("Phone number should be specified!!!")
        if not username:
            raise ValueError("Username should be specified!!!")
        if not password:
            raise ValueError("Password should be specified!!!")
        if not email:
            raise ValueError("Email should be specified!!!")
        self._set_password(password)
        user = self.model(username=username, phone_number=phone_number, password=self._password, email=email, **other)
        user.save(using=self.db)
        return user

    def create_user(self, username, phone_number, password, email, **other):
        other.setdefault("is_user", True)
        other.setdefault("is_partner", False)
        self._create_user(self, username, phone_number, password, email, **other)

    def create_partner(self, username, phone_number, password, email, **other):
        other.setdefault("is_user", False)
        other.setdefault("is_partner", True)
        self._create_user(self, username, phone_number, password, email, **other)

    def check_password(self, password):
        return make_password(password) == make_password(self._password)


class VivaroUser(models.Model):
    name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=150)
    username = models.CharField(max_length=100, blank=False, default=None)
    email = models.EmailField(max_length=200, blank=False, default=None)
    password = models.CharField(max_length=200, blank=False, default=None)
    phone_number = models.CharField(max_length=100, blank=False, default=None)
    balance = models.IntegerField(default=0)
    bonus = models.FloatField(default=0.0)
    is_authenticated = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
