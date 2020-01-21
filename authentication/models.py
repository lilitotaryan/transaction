from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone

from authentication.utils import UserAccountAction, get_current_time


class UserManager(models.Manager):
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
            user.save()
        except Exception as e:
            print(e)
            raise ValueError("User already exists")
        return user

    def create_user(self, **other):
        return self._create_user(**other)

class User(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100, blank=False, default=None, unique=True)
    email = models.EmailField(max_length=200, blank=False, default=None, unique=True)
    password = models.CharField(max_length=200, blank=False, default=None)
    phone_number = models.CharField(max_length=100, blank=False, default=None, unique=True)
    is_authenticated = models.BooleanField(default=False)
    balance = models.FloatField(default=0.0)
    bonus = models.IntegerField(default=0)
    objects = UserManager()

    def check_password(self, password):
        return make_password(password, salt="salt") == self.password

    def unauthenticate(self):
        self.is_authenticated = False
        self.save()

    def authenticate(self):
        self.is_authenticated = True
        self.save()


class Device(models.Model):
    os_family = models.StringField(max_length=STRING_LEN)
    os_version = models.StringField(max_length=STRING_LEN)
    device_brand = models.StringField(max_length=STRING_LEN)
    device_model = models.StringField(max_length=STRING_LEN)
    device_id = models.StringField(max_length=STRING_LEN, unique=True)
    is_tablet = models.BooleanField(default=False)
    user_agent = models.StringField(max_length=STRING_LEN)
    user = models.models.ForeignKey(User, models.CASCADE)



class UserAction(models.Model):
    email = models.EmailField(max_length=100, required=True)
    action = models.IntegerField(required=True, choices=UserAccountAction.choices())
    ip = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    device = models.ForeignKey(Device, models.CASCADE, null=True)
    time = models.DateTimeField(default=get_current_time)
    params = models.DictField()



class Session(models.Model):
    token = models.UUIDField(unique=True)
    last_date = models.DateTimeField(default=timezone.datetime.now())
    is_expired = models.DateTimeField(null=True)
    user = models.ForeignKey(User, models.CASCADE, null=True)
    action = models.ForeignKey(UserAction, models.CASCADE, null=True)
    device = models.ForeignKey(Device, models.CASCADE, null=True)
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
        user = User.objcets.create(**data)
        self.user = user
        user.save()
        self.save()

    def create_action(self, data):
        action = UserAction.objcets.create(**data)
        self.action = action
        action.save()
        self.save()
