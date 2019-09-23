from rest_framework import serializers
from .models import VivaroUser


class MoneyTransactionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    balance = serializers.IntegerField(required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, from_user, validated_data):
        user = VivaroUser.objects.get(username = validated_data.get("username"))
        if user:
            user.change_balance(1, validated_data.get("balance"))
            from_user.change_balance(-1, validated_data.get("balance"))
            return True
        return False

class BonusTransactionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    bonus = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, from_user, validated_data):
        user = VivaroUser.objects.get(username=validated_data.get("username"))
        if user:
            user.add_bonus_balance(validated_data.get("bonus"))
            return True
        return False
