from rest_framework import serializers
from .models import VivaroUser, Partner


class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    partner_id = serializers.CharField(max_length=25, required=True)
    partner_balance = serializers.FloatField(required=False)
    balance = serializers.FloatField(required=False, default=0.0)
    bonus = serializers.IntegerField(required=False, default=0)

    def create(self, validated_data):
        data = {'partner_id': validated_data.pop('partner_id'),
                'partner_balance': validated_data.pop('partner_balance', 0.0)}
        user = VivaroUser.objects.create_user(**validated_data)

        # try:
        #     # account = Account.objects.create(account_number=user_account_number, currency=user_account_currency)
        # except Exception as e:
        #     print(e)
        # account.add_user(user)
        user.add_partner(**data)
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
