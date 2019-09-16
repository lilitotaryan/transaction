from rest_framework import serializers
from .models import VivaroUser


class UserRegestrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=150)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    balance = serializers.IntegerField(default=0)
    bonus = serializers.FloatField(default=0.0)
    is_authenticated = serializers.BooleanField(default=False)
    is_partner = serializers.BooleanField(default=False)
    is_user = serializers.BooleanField(default=False)

    def create(self, validated_data):
        if validated_data.get('is_partner'):
            return VivaroUser.create_partner(**validated_data)
        return VivaroUser.create_user(**validated_data)

    def update(self, instance, validated_data):
        pass


class VivaroUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def authentication(self, validated_data):
        try:
            user = VivaroUser.get(username=validated_data.get('username'))
            if user.check_password(validated_data.get('password')):
                user.is_authenticated = True
                user.save()
                return True
            return False
        except VivaroUser.DoesNotExist:
            return False

class MoneyTransactionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    amount = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, validated_data):
        user = validated_data.get("username")
        if user:
            user.balance = user.balance + validated_data.amount
            user.save()
            return True
        return False

class BonusTransactionSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    bonus = serializers.IntegerField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def transfer(self, validated_data):
        user = validated_data.get("username")
        if user:
            user.bonus = user.bonus + validated_data.bonus
            user.save()
            return True
        return False
