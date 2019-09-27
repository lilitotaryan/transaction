from django.db import models
from django.utils import timezone
from authentication.models import VivaroUser, Session, Partner

# if bonus the currency is equal to bonus
class Transaction(models.Model):
    user = models.ForeignKey(VivaroUser, models.CASCADE, null=True)
    partner = models.ForeignKey(Partner, models.CASCADE, null=True)
    send_date = models.DateTimeField(default=timezone.datetime.now())
    receive_date = models.DateTimeField(default=timezone.datetime.now())
    amount = models.FloatField(default=0.0)
    send = models.BooleanField(default=False)
    ongoing = models.BooleanField(default=False)
    currency = models.CharField(max_length=5, blank=False, default=None)

    def sent(self):
        self.send = True
        self.save()

    def set_send_date(self):
        if self.ongoing:
            self.send_date = models.DateTimeField(default=timezone.datetime.now())
            self.save()

    def set_receive_date(self):
        if self.send:
            self.receive_date = models.DateTimeField(default=timezone.datetime.now())
            self.save()

    def add_user(self, user):
        self.user = user
        self.save()

    def add_partner(self, partner):
        self.partner = partner
        self.save()


# class Account(models.Model):
#     account_number = models.CharField(max_length=25, blank=False, default=None, unique=True)
#     user = models.ForeignKey(VivaroUser, models.CASCADE)
#     partner = models.ForeignKey(Partner, models.CASCADE, null=True)
#     transaction = models.ForeignKey(Transaction, models.CASCADE)
#     balance = models.FloatField(default=0.0)
#     bonus = models.IntegerField(default=0)
#     currency = models.CharField(max_length=5, blank=False, default=None)
#
#     def balance_change(self, amount):
#         self.balance = self.balance + amount
#         self.save()
#
#     def bonus_change(self, amount):
#         self.bonus = self.bonus + amount
#         self.save()
#
#     def create_transaction(self, data):
#         transaction = Transaction.objects.create(**data)
#         self.transaction = transaction
#         transaction.save()
#         self.save()
#
#     def create_user(self, data):
#         user = VivaroUser.objects.create(**data)
#         self.user = user
#         user.save()
#         self.save()
#
#     def create_partner(self, data):
#         partner = Partner.objects.create(**data)
#         self.partner = partner
#         partner.save()
#         self.save()
#
#     def add_user(self, user):
#         self.user = user
#         self.save()
#
#     def add_partner(self, partner):
#         self.partner = partner
#         self.save()
