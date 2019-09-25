from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Partner(models.Model):
    partner_id = models.CharField(max_length=25)


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
        other['password'] = self._password
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
    is_authenticated = models.BooleanField(default=False)
    partner = models.ForeignKey(Partner, models.CASCADE)
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
        self.balance = self.balance + (operator) * amount
        self.save()

    def add_bonus(self, amount):
        self.balance = self.balance + amount
        self.save()

class UserAction(models.Model):
    logged_in = models.BooleanField(default=False)
    logged_out = models.BooleanField(default=False)

    def user_logged_in(self):
        self.logged_in = True
        self.logged_out = False
        self.save()

    def user_logged_out(self):
        self.logged_out = True
        self.logged_in = False
        self.save()

class Session(models.Model):
    token = models.UUIDField(unique=True)
    last_date = models.DateTimeField(default=timezone.datetime.now())
    is_expired = models.DateTimeField(null=True)
    user = models.ForeignKey(VivaroUser, models.CASCADE)
    action = models.ForeignKey(UserAction, models.CASCADE)

    def update_last_date(self):
        self.last_date = timezone.datetime.now()
        self.save()

    def expire(self):
        self.expired_date = self.last_date
        self.is_expired = True
        self.save()

    def unexpire(self):
        self.is_expired = False
        self.save()

    def is_unexpired(self):
        if timezone.datetime.now().minute <= self.last_date.minute + 30:
            return True
        self.expire()
        return False

    def expire_all_sessions(self):
        all = Session.objects.filter(is_expired=False)
        if all:
            for i in all:
                i.expire()

    def create_user(self, data):
        user = VivaroUser.objcets.create(**data)
        self.user = user
        user.save()
        self.save()

    def create_action(self, data):
        action = UserAction.objcets.create(**data)
        self.action = action
        action.save()
        self.save()
