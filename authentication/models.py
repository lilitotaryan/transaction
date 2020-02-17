import uuid
from django.db.utils import IntegrityError
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager

from authentication.errors import UserAlreadyExists
from authentication.utils import get_current_time
from constants import SESSION_EXPIRATION_TIME


class Address(models.Model):
    address1 = models.CharField(max_length=100, blank=False, default=None)
    address2 = models.CharField(max_length=100, blank=False, default=None)
    city = models.CharField(max_length=100, blank=False, default=None)
    state = models.CharField(max_length=100, blank=False, default=None)
    zip_code = models.CharField(max_length=100)
    hash = models.UUIDField(unique=True, blank=False, default=None)

    def serialize(self):
        return {"address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "state": self.state,
                "zip_code": self.zip_code}

    def create(self, kwargs):
        hash = uuid.uuid3(uuid.NAMESPACE_DNS, kwargs.get("address1")+kwargs.get("city")+
                               kwargs.get("address2")+kwargs.get("state"))
        kwargs["hash"] = hash
        super().objects.create(**kwargs)

class CustomUserManager(UserManager):

    def _create_user(self, **other):
        phone_number = other.get('phone_number')
        password = other.get('password')
        email = other.get('email')
        user = self.model(**other)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except IntegrityError:
            raise UserAlreadyExists()
        return user

    def create_user(self, other):
        other.setdefault('is_staff', False)
        other.setdefault('is_superuser', False)
        return self._create_user(**other)


    def create_superuser(self, other):
        other.setdefault('is_staff', True)
        other.setdefault('is_superuser', True)

        if other.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if other.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(**other)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(max_length=200, blank=False, default=None, unique=True)
    password = models.CharField(max_length=200, blank=False, default=None)
    phone_number = models.CharField(max_length=100, blank=False, default=None, unique=True)
    address = models.ForeignKey(Address, models.CASCADE, null=True)
    gender = models.CharField(max_length=1, default="F", choices=[("M", "Male"),
                                                                  ("F", "Female"),
                                                                  ("O", "Other")])
    is_varified = models.BooleanField(default=False)
    is_termsandconditions_accepted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=get_current_time)
    name = models.CharField(max_length=200, default=None, unique=True, null=True)
    birth_date = models.DateField(null=True)

    is_company = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def serialize(self, address=False, category=False):
        res = {"first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number,
                "gender": self.gender,
                "email": self.email,
                "birth_date": self.birth_date,
                "is_varified": self.is_varified,
                "is_termsandconditions_accepted": self.is_termsandconditions_accepted,
                "address": self.address.serialize() if address and self.address else "",
                "is_company": self.is_company,
                }
        if self.is_company:
            res["name"] = self.name if self.is_company else "",
        else:
            res["category"] = [category.serialize() for category in Category.objects.get(user=self)] \
                                  if category else [],
        return res


class Category(models.Model):
    # todo check for is it possible to have same name for different users how db stores it
    name = models.CharField(max_length=100, blank=False, default=None, unique=True)
    description = models.CharField(max_length=500)
    user = models.ForeignKey(CustomUser, on_delete=False, null=True)

    def serialize(self):
        return {"name": self.name,
                "description": self.description
                }


class CreditCard(models.Model):
    card_number = models.CharField(max_length=100, blank=False, default=None, unique=True)
    css_ccv = models.CharField(max_length=100, blank=False, default=None)
    first_name = models.CharField(max_length=100, blank=False, default=None)
    last_name = models.CharField(max_length=100, blank=False, default=None)
    card_expiration_date = models.DateField(blank=False)
    user = models.ForeignKey(CustomUser, models.CASCADE, null=True)

    def serialize(self):
        return {"card_number": self.card_number,
                "css_ccv": self.css_ccv,
                "first_name": self .first_name,
                "last_name": self.last_name,
                "card_expiration_date": self.card_expiration_date
                }


class Session(models.Model):
    token = models.UUIDField(unique=True, blank=False, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, models.CASCADE, null=True)
    device_brand = models.CharField(max_length=200, blank=False, default=None)
    os_system = models.CharField(max_length=200, blank=False, default=None)
    disconnected_date = models.DateTimeField(default=get_current_time)
    connected_date = models.DateTimeField(default=get_current_time)
    is_expired = models.BooleanField(default=False)

    def is_unexpired(self):
        if get_current_time().minute <= self.connected_date.minute + SESSION_EXPIRATION_TIME:
            return True
        self.is_expired = True
        self.disconnected_date = get_current_time()
        self.save()
        return False

    def expire_session(self):
        self.is_expired = True
        self.disconnected_date = get_current_time()
        self.save()

    @staticmethod
    def expire_all_sessions(self):
        sessions = Session.objects.filter(is_expired=False)
        if sessions:
            [i.expire() for i in sessions]

