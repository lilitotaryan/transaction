from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegestrationSerializer, MoneyTransactionSerializer, BonusTransactionSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response


@api_view(['POST'])
def regestration(request):
    data = UserRegestrationSerializer(data=request.data)
    if data.is_valid():
            try:
                user = data.create(data.validated_data)
                print(user)
                return Response("Success")
            except:
                return Response({"error": "User already exists"}, status=404)
    return Response({"error": "All the fields should be specified"}, status=404)


@api_view(['POST'])
def login(request):
    data = VivaroUserLoginSerializer(data=request.data)
    if data.is_valid():
        user = data.authentication(data.validated_data)
        if user:
            user.is_authenticated = True
            request.user = user
            user.save()
            return Response({"username": user.username, "email": user.email, "phone_number": user.phone_number})
    return Response({"error": "Invalid username or password"}, status=404)


def logout(request):
    if request.user:
        request.user.is_authenticated = False
        request.user = None
        return Response("Success")
    return Response({"error": "No user is logged in"}, status=404)

class MoneyTransaction(APIView):
    def put(self, request):
        if request.user:
            if request.user.is_partner:
                data = MoneyTransactionSerializer(data=request.data)
                if data.is_valid():
                    if not data.transfer(data.validated_data):
                        return Response({"error": "Username does not exist"}, status=404)
                return Response({"error": "Invalid input"}, status=404)
        return Response({"error": "No partner is logged in"}, status=404)


@api_view(['PUT'])
def bonus_transaction(request):
    if request.user:
        if request.user.is_partner:
            data = BonusTransactionSerializer(data=request.data)
            if data.is_valid():
                if not data.transfer(data.validated_data):
                    return Response({"error": "Username does not exist"}, status=404)
                return Response({"error": "Invalid input"}, status=404)
        return Response({"error": "No partner is logged in"}, status=404)