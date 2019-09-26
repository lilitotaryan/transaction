from rest_framework.views import APIView
from .serializers import TransactionSerializer
from rest_framework.response import Response
from authentication.permissions import CheckApiToken
from .permissions import PartnerPermission, CheckServiceToken
from .errors import IncompatibleCurrencies
from authentication.errors import InvalidInput, UserNotFound
from authentication.utils import error_handler

class Transaction(APIView):
    permission_classes = [CheckApiToken, CheckServiceToken, PartnerPermission]

    def post(request):
        data = TransactionSerializer(data=request.data)
        if data.is_valid():
            try:
                data.transfer(data.validated_data)
                return Response({"Success"}, status=200)
            except UserNotFound:
                return error_handler(UserNotFound)
            except IncompatibleCurrencies:
                return error_handler(IncompatibleCurrencies)
        return error_handler(InvalidInput)



