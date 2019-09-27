from rest_framework import serializers
from authentication.models import VivaroUser, Partner
from .models import Transaction
from .errors import IncompatibleCurrencies
from authentication.errors import UserNotFound


class TransactionSerializer(serializers.Serializer):
    partner_id = serializers.CharField(max_length=25, required=True)
    amount = serializers.FloatField(default=0.0)
    currency = serializers.CharField(max_length=5, required=True)
    username = serializers.CharField(max_length=100, required=True)
    partner_account = serializers.CharField(max_length=25, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, validated_data):
        partner = Partner.objects.get(partner_id=validated_data.get("partner_id"))
        user = VivaroUser.objects.filter(username=validated_data.get("username"), partner=partner)
        # partner_account = Account.objects.filter(account_number=validated_data.get("partner_account"), partner=partner)
        currency = validated_data.get("currency")
        # user_account = Account.objects.filter(user=user, currency=currency)[0]
        amount = validated_data.get("amount")
        if not user:
            raise UserNotFound
        # if partner_account.currency == currency:
        if currency != "bonus":
            user.balance_change(amount)
            partner.balance_change(-amount)
            return True
        user.bonus_change(amount)
        return True
        raise IncompatibleCurrencies
