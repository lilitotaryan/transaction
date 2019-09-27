from .serializers import VivaroUserLoginSerializer, UserRegistrationSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Session
from .permissions import AuthenticatedPermission, AlreadyAuthenticatedPermission, CheckApiToken
from .errors import UserAlreadyExists, InvalidInput, InvalidUsernamePassword, SessionAlreadyExpired
from .utils import error_handler

class Registration(APIView):
    # CheckApiToken,
    permission_classes = [AlreadyAuthenticatedPermission]

    def post(self, request):
        data = UserRegistrationSerializer(data=request.data)
        if data.is_valid():
                try:
                    data.create(data.validated_data)
                except:
                    return error_handler(UserAlreadyExists)
                return Response("Success")
        return error_handler(InvalidInput)


class Login(APIView):
    permission_classes = [AlreadyAuthenticatedPermission]

    def post(self, request):
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
                return InvalidInput(InvalidUsernamePassword)
        return error_handler(InvalidInput)


class Logout(APIView):
    permission_classes = [AuthenticatedPermission]

    def post(self, request):
        session = Session.objects.get(token=request.data.get("session_token"))
        user = session.user
        if session.is_unexpired():
            session.action.logged_out()
            session.expire_all_sessions()
            user.unauthenticate()
            return Response("Success")
        return error_handler(SessionAlreadyExpired)

