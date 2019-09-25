from rest_framework import serializers
from .models import VivaroUser, Partner
from pay.models import Account

class UserRegistrationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=150, required=False)
    username = serializers.CharField(max_length=100, required=True)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    is_authenticated = serializers.BooleanField(default=False, required=False)
    partner_id = serializers.CharField(max_length=25, required=True)
    account_number = serializers.CharField(max_length=25, required=True)
    account_currency = serializers.CharField(max_length=5, required=True)

    def create(self, validated_data):
        partner_id = validated_data.pop('partner_id')
        account_number = validated_data.pop('account')
        user = VivaroUser.objects.create_user(**validated_data)
        account = Account.objects.create(account_number=account_number, currency=validated_data.get('account_currency'))
        account.add_user(user)
        user.add_partner(partner_id)
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

class CreatePartnerSerializer(serializers.Serializer):
    partner_id = serializers.CharField(max_length=25, required=True, unique=True)
    account_number = serializers.CharField(max_length=25, required=True)
    account_currency = serializers.CharField(max_length=5, required=True)

    def create(self, validated_data):
        partner_id = validated_data.pop('partner_id')
        account_number = validated_data.pop('account')
        partner = Partner.objects.create(**validated_data)
        account = Account.objects.create(account_number=account_number, currency=validated_data.get('account_currency'))
        account.add_partner(partner)
        return partner

    def update(self, instance, validated_data):
        pass