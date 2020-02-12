import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, UserManager
from authentication.utils import get_current_time
from constants import STRING_LEN, SESSION_EXPIRATION_TIME

class Address(models.Model):
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    zip_code = models.CharField(max_length=100)

    def serialize(self):
        return {"address1": self.address1,
                "address2": self.address2,
                "city": self.city,
                "state": self.state,
                "zip_code": self.zip_code}

class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, default=None, unique=True)
    description = models.CharField(max_length=500)

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


class CustomUserManager(UserManager):

    def _create_user(self, **other):
        phone_number = other.get('phone_number')
        password = other.get('password')
        email = other.get('email')
        if not phone_number:
            raise ValueError("Phone number should be specified!!!")
        if not password:
            raise ValueError("Password should be specified!!!")
        if not email:
            raise ValueError("Email should be specified!!!")
        user = self.model(**other)
        user.set_password(password)
        try:
            user.save(using=self._db)
        except Exception as e:
            print(e)
            raise ValueError("User already exists")
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
    email = models.EmailField(max_length=200, blank=False, default=None, unique=True, primary_key=True)
    password = models.CharField(max_length=200, blank=False, default=None)
    phone_number = models.CharField(max_length=100, blank=False, default=None, unique=True)
    address = models.OneToOneField(Address, models.CASCADE, null=True)
    card = models.ForeignKey(CreditCard, models.CASCADE, null=True)
    gender = models.CharField(max_length=1, default="F", choices=[("M", "Male"),
                                                                  ("F", "Female"),
                                                                  ("O", "Other")])
    is_varified = models.BooleanField(default=False)
    is_tearmsandconditions_accepted = models.BooleanField(default=False)
    created_date = models.DateTimeField(default=get_current_time)
    name = models.CharField(max_length=200, default=None, unique=True, null=True)
    category = models.ForeignKey(Category, models.CASCADE, null=True)
    is_company = models.BooleanField(default=False)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def serialize(self, address=False):
        return {"first_name": self.first_name,
                "last_name": self.last_name,
                "phone_number": self.phone_number,
                "gender": self.gender,
                "email": self.email,
                "is_varified": self.is_varified,
                "is_tearmsandconditions_accepted": self.is_tearmsandconditions_accepted,
                "address": self.address.serialize() if address else "",
                "name": self.name if self.is_company else "",
                "is_company": self.is_company
                }

# class EventUser(models.Model):
#     category = models.ForeignKey(Category, models.CASCADE, null=True)
#     credentials = models.OneToOneField(CustomUser, models.CASCADE, null=True)
#
#     @classmethod
#     def create(cls, other):
#         cls(self.credentials.objects.create_user(other))
#         return
#
#     def serialize(self, address=False):
#         result = dict(**self.credentials.serialize(address))
#         result["is_event_user"] = True
#         return result
#
#     class Meta:
#         verbose_name = 'EventUser'
#
#
# class Company(models.Model):
#     name = models.CharField(max_length=200, blank=False, default=None, unique=True)
#     credentials = models.OneToOneField(CustomUser, models.CASCADE)
#
#     @classmethod
#     def create(cls, other):
#         return super().objects.create_user(other)
#
#     def serialize(self, address=False):
#         result = dict(**self.credentials.serialize(address))
#         result["is_company_user"] = True
#         result["name"] = self.name
#         return result
#
#     class Meta:
#         verbose_name = 'Company'
#         verbose_name_plural = 'Companies'


# class Admin(CustomUser):
#     pass
    # def create_user(self, other):
    #     return super().create_superuser(other)


class Session(models.Model):
    token = models.UUIDField(unique=True, blank=False, default=uuid.uuid4)
    user = models.ForeignKey(CustomUser, models.CASCADE, null=True)
    device_brand = models.CharField(max_length=200, blank=False, default=None)
    os_system = models.CharField(max_length=200, blank=False, default=None)
    disconnected_date = models.DateTimeField(default=get_current_time)
    connected_date = models.DateTimeField(default=get_current_time)
    is_expired = models.BooleanField(default=False)

    def is_unexpired(self):
        if get_current_time.minute <= self.last_date.minute + SESSION_EXPIRATION_TIME:
            return True
        self.is_expired = True
        self.disconnected_date = get_current_time()
        self.save()
        return False

    @staticmethod
    def expire_all_sessions(self):
        all = Session.objects.filter(is_expired=False)
        if all:
            for i in all:
                i.expire()

