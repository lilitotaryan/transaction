from django.contrib.auth import authenticate, login, logout

from .serializers import UserRegistrationSerializer, UserLoginSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Session
# from .permissions import AuthenticatedPermission, AlreadyAuthenticatedPermission, CheckApiToken
from .errors import InvalidUsernamePassword, SessionAlreadyExpired
from .utils import error_handler


class User(APIView):
    permission_classes = []

    def post(self, request):
        data = UserRegistrationSerializer(data=request.data)
        if data.is_valid():
            user = data.create(validated_data=data.validated_data)
            if user is not None:
                return Response({"username": user.username, "email": user.email, "phone_number": user.phone_number})
            return Response({"error": "could not register user"})
        return Response({"error": "could not register user from serializer"})

    def get(self, request):
        return request.user

    def delete(self, request):
        pass

    def patch(self, request):
        pass



class Login(APIView):
    permission_classes = []

    def post(self, request):
        data = UserLoginSerializer(data=request.data)
        if data.is_valid():
            email=data.validated_data.get("email")
            password = data.validated_data.get("password")
            user = authenticate(email=email,
                                password=password)
            if user is not None:
                login(request, user)
                session = Session(user=user, device_brand=request.data.get('device_brand'),
                                  os_system=request.data.get('os_system'))
                session.save()
                request.user.session = session.token
                return Response(user.serialize())
            return Response({"error": "Invalid Username or Password"})

class Logout(APIView):
    permission_classes = []

    # def post(self, request):
    #     session = Session.objects.get(token=request.data.get("session_token"))
    #     user = session.user
    #     if session.is_unexpired():
    #         session.action.logged_out()
    #         session.expire_all_sessions()
    #         user.unauthenticate()
    #         return Response("Success")
    #     return error_handler(SessionAlreadyExpired)

    def get(self, request):
        logout(request)
        return Response({"success": "true"})
