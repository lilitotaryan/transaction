from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegestrationSerializer, MoneyTransactionSerializer, BonusTransactionSerializer
from rest_framework.decorators import api_view
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAction, VivaroUser, Session

@api_view(['POST'])
def regestration(request):
    data = UserRegestrationSerializer(data=request.data)
    if data.is_valid():
            try:
                user = data.create(data.validated_data)
                return Response("Success")
            except:
                return Response({"error": "User already exists"}, status=400)
    return Response({"error": "All the fields should be specified"}, status=400)


@api_view(['POST'])
def login(request):
    data = VivaroUserLoginSerializer(data=request.data)
    if data.is_valid():
        session = Session.objects.get(token = request.data.get("session_token"))
        user = data.authentication(data.validated_data)
        session.add_user(user)
        expired = session.is_unexpired()
        if user and not expired:
            if not session.user_action:
                session.user_action.add_action({"logged_in": True, "logged_out": False})
            elif session.user_action.logged_out:
                session.user_action.user_logged_in()
                session.update_last_date()
                user.authenticate()
                return Response({"username": user.username, "email": user.email, "phone_number": user.phone_number})
            return Response({"error": "User is already logged in"}, status=402)
        if not user:
            return Response({"error": "Invalid username or password"}, status=404)
        if expired:
            return Response({"error": "User is already logged in"}, status=402)
    return Response({"error": "Invalid input"}, status=400)


@api_view(['POST'])
def logout(request):
    session = Session.objects.get(token = request.data.get("session_token"))
    user = session.user
    if not user or not session.action or not session.action.logged_in:
        return Response({"error": "No user is logged in"}, status=404)
    if not session:
        return Response({"error": "No user is logged in anymore the session expired"}, status=404)
    if user and session and session.is_unexpired() and session.action.logged_in:
        session.action.logged_out()
        session.expire_all_sessions()
        user.unauthenticate()
        return Response("Success")


class MoneyTransaction(APIView):
    def put(self, request):
        try:
            session = Session.objects.get(token=request.data.get("session_token"))
            user = session.user
            UserAction.objects.get(loged_in=True)
        except UserAction.DoesNotExist or VivaroUser.DoesNotExist or Session.DoesNotExist:
            return Response({"error": "No user is logged in"}, status=404)
        if user.is_partner:
            data = MoneyTransactionSerializer(data=request.data)
            if data.is_valid():
                if not data.transfer(user, data.validated_data):
                    return Response({"error": "Username does not exist"}, status=404)
                return Response({"Success"})
            return Response({"error": "Invalid input"}, status=400)
        return Response({"error": "No partner is logged in"}, status=403)


@api_view(['PUT'])
def bonus_transaction(request):
    try:
        session = Session.objects.get(token=request.data.get("session_token"))
        user = session.user
        UserAction.objects.get(loged_in=True)
    except UserAction.DoesNotExist or VivaroUser.DoesNotExist or Session.DoesNotExist:
        return Response({"error": "No user is logged in"}, status=404)
    if user.is_partner:
        data = BonusTransactionSerializer(data=request.data)
        if data.is_valid():
            if not data.transfer(user, data.validated_data):
                return Response({"error": "Username does not exist"}, status=404)
            return Response({"Success"})
        return Response({"error": "Invalid input"}, status=400)
    return Response({"error": "No partner is logged in"}, status=403)