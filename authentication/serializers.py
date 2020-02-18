import uuid

from rest_framework import serializers
from .models import CustomUser, Address, Category


class UserRegistrationSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=100, required=False)
    last_name = serializers.CharField(max_length=100, required=False)
    email = serializers.EmailField(max_length=200, required=True)
    password = serializers.CharField(max_length=200, required=True)
    phone_number = serializers.CharField(max_length=100, required=True)
    gender = serializers.ChoiceField(choices=["M", "Male", "F", "Female", "O", "Other"], required=False)
    is_termsandconditions_accepted = serializers.BooleanField()
    birth_date = serializers.DateField(default=None, required=False)
    is_company = serializers.BooleanField(default=False)

    def create(self, validated_data):
        return CustomUser.objects.create_user(validated_data)

    def update(self, instance, validated_data):
        pass


class CompanyRegistrationSerializer(UserRegistrationSerializer):
    name = serializers.CharField(max_length=200, required=True)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=100, required=True)
    password = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class SessionRecordSerializer(serializers.Serializer):
    device_brand = serializers.CharField(max_length=200, required=True)
    os_system = serializers.CharField(max_length=200, required=True)

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class CategoryAddSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=True)
    description = serializers.CharField(max_length=500)

    def create(self, validated_data):
        return Category.objects.create(validated_data)

    def update(self, instance, validated_data):
        pass


class AddressCreationSerializer(serializers.Serializer):
    address1 = serializers.CharField(max_length=100, required=True)
    address2 = serializers.CharField(max_length=100, required=True)
    city = serializers.CharField(max_length=100, required=True)
    state = serializers.CharField(max_length=100, required=True)
    zip_code = serializers.CharField(max_length=100)

    def create(self, validated_data):
        return Address.create(validated_data)

    def update(self, instance, validated_data):
        pass

    @staticmethod
    def get_hash(validated_data):
        return uuid.uuid3(uuid.NAMESPACE_DNS, validated_data.get("address1") + validated_data.get("city") +
                          validated_data.get("address2") + validated_data.get("state"))

