from django.contrib.auth import authenticate, logout
from rest_framework.decorators import permission_classes
from rest_framework.authtoken.models import Token

from authentication.decorators import error_handler
from .permissions import SessionExpiredPermission, ApiTokenPermission, LoggedInPermission, LoggedInNotVerifiedPermission
from .serializers import UserRegistrationSerializer, UserLoginSerializer, SessionRecordSerializer, \
    CompanyRegistrationSerializer, CategoryAddSerializer, AddressCreationSerializer, UserUpdateSerializer, \
    UserValidationTokenSerializer
from rest_framework.views import APIView
from .models import Session, Category, Address
from django.conf import settings
from .errors import InvalidUsernamePassword, SessionAlreadyExpired, DeviceDataNotValid, UserDataNotValid, \
    CategoryDataNotValid, CategoriesNotFound, AddressDataNotValid, UserHasNoCategory, \
    UserHasNoAddress, InvalidEmailValidationToken
from .utils import response, send_verification_email


class User(APIView):

    @error_handler
    def post(self, request):
        if not request.data.get("is_company"):
            data = UserRegistrationSerializer(data=request.data)
        else:
            data = CompanyRegistrationSerializer(data=request.data)
        if data.is_valid():
            user = data.create(validated_data=data.validated_data)
            if user is not None:
                return response(data=user.serialize())
        # Todo not mandatory for serializer errors
        # for key, val in data.errors:
        #     field = key
        #     for i in val:
        #         # map(lambda d: d['value'], l)
        #         code = val[i].code
        #             raise VallidationError(field, code)
        raise UserDataNotValid()

    @error_handler
    def get(self, request):
        return response(request.user.serialize())

    @error_handler
    def delete(self, request):
        user = request.user
        session = Session.objects.get(token=request.META.get('HTTP_USER_SESSION'))
        session.expire_all_sessions()
        user.is_active = False
        user.save()
        return response()

    @error_handler
    def patch(self, request):
        user = request.user
        request_data = request.data
        if request_data:
            data = UserUpdateSerializer(data=request_data)
            if data.is_valid():
                user = data.update(instance=user, validated_data=data.validated_data)
                if user is not None:
                    return response()
            # Todo not mandatory for serializer errors
            # for key, val in data.errors:
            #     field = key
            #     for i in val:
            #         # map(lambda d: d['value'], l)
            #         code = val[i].code
            #             raise VallidationError(field, code)
            raise UserDataNotValid()
        raise UserDataNotValid()

    def get_permissions(self):
        if self.request.method == 'POST':
            permission_classes = [ApiTokenPermission]
        else:
            permission_classes = [ApiTokenPermission, LoggedInPermission, SessionExpiredPermission]
        return [permission() for permission in permission_classes]


class Login(APIView):
    permission_classes = [ApiTokenPermission]

    @error_handler
    def post(self, request):
        session_request = {'device_brand': request.data.pop('device_brand', None),
                           'os_system': request.data.pop('os_system', None)
                           }
        data = UserLoginSerializer(data=request.data)
        session_data = SessionRecordSerializer(data=session_request)
        if not session_data.is_valid() and settings.DEBUG:
            raise DeviceDataNotValid()
        if data.is_valid():
            email = data.validated_data.get("email")
            password = data.validated_data.get("password")
            user = authenticate(email=email,
                                password=password)
            if user is not None:
                token, _ = Token.objects.get_or_create(user=user)
                session = Session(user=user, device_brand=session_data.validated_data.get('device_brand'),
                                  os_system=session_data.validated_data.get('os_system'))
                session.save()
                data = {
                    "session_token": session.token,
                    "auth_token": token.key,
                    "is_verified": user.is_verified
                }
                return response(data=data)
            raise InvalidUsernamePassword()


class Logout(APIView):
    permission_classes = [ApiTokenPermission, LoggedInPermission, SessionExpiredPermission]

    @error_handler
    def get(self, request):
        session = Session.objects.get(token=request.META.get('HTTP_USER_SESSION'))
        session.expire_session()
        logout(request)
        return response()


class UserCategory(APIView):
    permission_classes = [ApiTokenPermission, LoggedInPermission, SessionExpiredPermission]

    @error_handler
    def post(self, request):
        user = request.user
        categories_data = request.data.get("categories")
        for i in categories_data:
            data = CategoryAddSerializer(data=i)
            if data.is_valid():
                category = Category.objects.get(name=data.validated_data("name"))
                if category is None:
                    category = data.create(data.validated_data)
                category.user.add(user)
                category.save()
            raise CategoryDataNotValid()

    @error_handler
    def get(self, request):
        user = request.user
        all_categories = Category.objects.get(user=user)
        if all_categories is not None:
            return response(data={[i.serialize() for i in all_categories]})
        raise UserHasNoCategory()

    def delete(self, request):
        pass


@error_handler
@permission_classes([ApiTokenPermission])
def get_all_categories(request):
    all_categories = Category.objects.values('name').distinct()
    if all_categories is not None:
        return response(data={[i.serialize for i in all_categories]})
    raise CategoriesNotFound()


class UserAddress(APIView):
    permission_classes = [ApiTokenPermission, LoggedInPermission, SessionExpiredPermission]

    @error_handler
    def post(self, request):
        user = request.user
        data = AddressCreationSerializer(data=request.data)
        if data.is_valid():
            address = Address.objects.get(hash=data.get_hash(data.validated_data))
            if address is None:
                address = data.create(data.validated_data)
            user.address.add(address)
            user.save()
        raise AddressDataNotValid()

    @error_handler
    def get(self, request):
        user = request.user
        all_addresses = user.objects.filter(address__in=Address)
        if all_addresses is not None:
            return response(data={[i.serialize for i in all_addresses]})
        raise UserHasNoAddress()

    def delete(self, request):
        pass


class EmailVerification(APIView):
    permission_classes = [ApiTokenPermission, LoggedInNotVerifiedPermission, SessionExpiredPermission]

    @error_handler
    def get(self, request):
        user = request.user
        if not request.GET.get('email_sent'):
            verification_token = user.get_verification_token()
            send_verification_email(user.email, verification_token)
            user.email_sent = True
            user.save()
            return response()
        else:
            verification_token = user.re_update_verification_token()
            send_verification_email(user.email, verification_token)
            user.email_sent = True
            user.save()
            return response()

    @error_handler
    def post(self, request):
        user = request.user
        token = UserValidationTokenSerializer(data=request.data)
        if token.is_valid():
            if not token.check_token(user, token.validated_data):
                raise InvalidEmailValidationToken()
            user.is_verified = True
            user.save()
            return response()
        raise InvalidEmailValidationToken()
