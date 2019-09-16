from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegestrationSerializer, MoneyTransactionSerializer, BonusTransactionSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView


@api_view(['POST'])
def regestration(request):
    data = UserRegestrationSerializer(data=request.data)
    if data.is_valid():
        return data.create(data.validated_data)
    raise ValueError("All fields are required")


@api_view(['POST'])
def login(request):
    data = VivaroUserLoginSerializer(data=request.data)
    if data.is_valid():
        user = data.authentication(data.validated_data)
        if user:
            user.is_authenticated = True
            request.user = user
            user.save()
            return user
    raise ValueError("Invalid username or password")


def logout(request):
    if request.user:
        request.user.is_authenticated = False
        request.user = None


class MoneyTransaction(APIView):
    def put(self, request):
        if request.user:
            if request.user.is_partner:
                data = MoneyTransactionSerializer(data=request.data)
                if data.is_valid():
                    if not data.transfer(data.validated_data):
                        raise ValueError("User does not exist")
                raise ValueError("Invalid input")
        raise SuspiciousOperation("No partner is logged in")


@api_view(['PUT'])
def bonus_transaction(request):
    if request.user:
        if request.user.is_partner:
            data = MoneyTransactionSerializer(data=request.data)
            if data.is_valid():
                if not data.transfer(data.validated_data):
                    raise ValueError("User does not exist")
            raise ValueError("Invalid input")
    raise SuspiciousOperation("No partner is logged in")