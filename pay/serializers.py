from rest_framework import serializers
from authentication.models import VivaroUser
from .models import Transaction, Account

# if bonus the currency is equal to bonus
class TransactionSerializer(serializers.Serializer):
    partner_id = serializers.CharField(max_length=25)
    amount = serializers.FloatField(default=0.0, )
    currency = serializers.CharField(max_length=5, required=True)
    username = serializers.CharField(max_length=100, required=True, unique = True)
    account = serializers.CharField(max_length=25, required=True, unique=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, from_user, validated_data):
        user = VivaroUser.objects.get(username = validated_data.get("username"))
        account = Account.objects.get(account_number = validated_data.get("account"))
        if user and account:
            user.change_balance(1, validated_data.get("balance"))
            from_user.change_balance(-1, validated_data.get("balance"))
            return True
        return False
