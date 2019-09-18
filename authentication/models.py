from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password


class VivaroUserManager(models.Manager):
    _password = None

    def _set_password(self, password):
        self._password = make_password(password, salt="salt")

    def _create_user(self, **other):
        username = other.get('username')
        phone_number = other.get('phone_number')
        password = other.get('password')
        email = other.get('email')
        if not phone_number:
            raise ValueError("Phone number should be specified!!!")
        if not username:
            raise ValueError("Username should be specified!!!")
        if not password:
            raise ValueError("Password should be specified!!!")
        if not email:
            raise ValueError("Email should be specified!!!")
        self._set_password(password)
        other['password']=self._password
        user = self.model(**other)
        try:
            user.save(using=self.db)
        except:
            raise ValueError("User already exists")
        return user

    def create_user(self, **other):
        other.setdefault("is_user", True)
        other.setdefault("is_partner", False)
        return self._create_user(**other)

    def create_partner(self, **other):
        other.setdefault("is_user", False)
        other.setdefault("is_partner", True)
        return self._create_user(**other)


class VivaroUser(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=False, default=None, unique=True)
    email = models.EmailField(max_length=200, blank=False, default=None, unique=True)
    password = models.CharField(max_length=200, blank=False, default=None)
    phone_number = models.CharField(max_length=100, blank=False, default=None, unique=True)
    balance = models.FloatField(default=0.0)
    bonus = models.IntegerField(default=0)
    is_authenticated = models.BooleanField(default=False)
    is_user = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    objects = VivaroUserManager()

    def check_password(self, password):
        return make_password(password, salt="salt") == self.password

    def unauthenticate(self):
        self.is_authenticated = False
        self.save()

    def authenticate(self):
        self.is_authenticated = True
        self.save()

    def change_balance(self, operator, amount):
        self.balance = self.balance + (operator)*amount
        self.save()

    def add_bonus(self, amount):
        self.balance = self.balance + amount
        self.save()

class UserAction(models.Model):
    loged_in = models.BooleanField(default=False)
    logged_out = models.BooleanField(default=False)
    user = models.ForeignKey(VivaroUser, models.CASCADE)

    def user_logged_in(self):
        self.loged_in = True
        self.logged_out = False
        self.save()

    def user_logged_out(self):
        self.loged_out = True
        self.logged_in = False
        self.save()

    def set_user(self, new_user):
        self.user = new_user