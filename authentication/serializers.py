from rest_framework import serializers
from .models import VivaroUser



class UserRegestrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    balance = serializers.IntegerField(default=0, required=False)
    bonus = serializers.FloatField(default=0.0, required=False)
    is_authenticated = serializers.BooleanField(default=False, required=False)
    is_partner = serializers.BooleanField(default=False, required=False)
    is_user = serializers.BooleanField(default=False, required=False)

    def create(self, validated_data):
        if validated_data.get('is_partner'):
            user = VivaroUser.objects.create_partner(**validated_data)
            return user
        user = VivaroUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        pass


class VivaroUserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100, required=True)
    password = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    def authentication(self, validated_data):
        try:
            user = VivaroUser.objects.get(username=validated_data.get('username'))
            if user.check_password(validated_data.get('password')):
                user.is_authenticated = True
                user.save()
                return user
            return False
        except VivaroUser.DoesNotExist:
            return False

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
