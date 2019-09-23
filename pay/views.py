from django.shortcuts import render
from .serializers import VivaroUserLoginSerializer, UserRegestrationSerializer, MoneyTransactionSerializer, BonusTransactionSerializer
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import SuspiciousOperation
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import UserAction, VivaroUser, Session
from .permissions import AuthenticatedPermission, AlreadyAuthenticatedPermission


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