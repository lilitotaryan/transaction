from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegistrationSerializer
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAction, VivaroUser, Session
from .permissions import AuthenticatedPermission, AlreadyAuthenticatedPermission


class Registration(APIView):
    permission_classses = [AlreadyAuthenticatedPermission]
    def post(self, request):
        data = UserRegistrationSerializer(data=request.data)
        if data.is_valid():
                try:
                    data.create(data.validated_data)
                except:
                    return Response({"error": "User already exists"}, status=400)
                return Response("Success")
        return Response({"error": "All the fields should be specified"}, status=400)


@api_view(['POST'])
@permission_classes([AlreadyAuthenticatedPermission])
def login(request):
    data = VivaroUserLoginSerializer(data=request.data)
    if data.is_valid():
        session = Session.objects.get(token=request.data.get("session_token"))
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
        if not user:
            return Response({"error": "Invalid username or password"}, status=404)
    return Response({"error": "Invalid input"}, status=400)


@api_view(['POST'])
@permission_classes([AuthenticatedPermission])
def logout(request):
    session = Session.objects.get(token=request.data.get("session_token"))
    user = session.user
    if session.is_unexpired():
        session.action.logged_out()
        session.expire_all_sessions()
        user.unauthenticate()
        return Response("Success")
    return Response({"error": "Session is already expired"}, status=404)


def create_partner(request):
    pass
