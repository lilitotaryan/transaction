from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegestrationSerializer, MoneyTransactionSerializer, BonusTransactionSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAction

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
        action = UserAction.objects.filter(user=user, loged_in=True)
        if user and not action:
            action = UserAction.objects.filter(user=user, loged_in=False).get()
            user.authenticate()
            action.user_logged_in()
            return Response({"username": user.username, "email": user.email, "phone_number": user.phone_number})
        if not user:
            return Response({"error": "Invalid username or password"}, status=404)
        return Response({"error": "User is already logged in"}, status=404)


@api_view(['POST'])
def logout(request):
    action = UserAction.objects.get(loged_in=True)
    user = UserAction.objects.get(loged_in=True).user
    if action and user:
        user.unauthenticate()
        action.user_logged_out()
        return Response("Success")
    return Response({"error": "No user is logged in"}, status=404)


class MoneyTransaction(APIView):
    def put(self, request):
        try:
            action = UserAction.objects.get(loged_in=True)
            user = UserAction.objects.get(loged_in=True).user
        except UserAction.DoesNotExist:
            return Response({"error": "No user is logged in"}, status=404)
        if user.is_partner:
            data = MoneyTransactionSerializer(data=request.data)
            if data.is_valid():
                if not data.transfer(user, data.validated_data):
                    return Response({"error": "Username does not exist"}, status=404)
                return Response({"Success"})
            return Response({"error": "Invalid input"}, status=404)
        return Response({"error": "No partner is logged in"}, status=404)


@api_view(['PUT'])
def bonus_transaction(request):
    try:
        action = UserAction.objects.get(loged_in=True)
        user = UserAction.objects.get(loged_in=True).user
    except UserAction.DoesNotExist:
        return Response({"error": "No user is logged in"}, status=404)
    if user.is_partner:
        data = MoneyTransactionSerializer(data=request.data)
        if data.is_valid():
            if not data.transfer(user, data.validated_data):
                return Response({"error": "Username does not exist"}, status=404)
            return Response({"Success"})
        return Response({"error": "Invalid input"}, status=404)
    return Response({"error": "No partner is logged in"}, status=404)