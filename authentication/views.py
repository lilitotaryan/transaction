from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import permission_classes

from authentication.decorators import error_handler
from .permissions import SessionExpiredPermission, ApiTokenPermission, LoggedInPermission
from .serializers import UserRegistrationSerializer, UserLoginSerializer, SessionRecordSerializer, \
    CompanyRegistrationSerializer, CategoryAddSerializer, AddressCreationSerializer
from rest_framework.views import APIView
from .models import Session, Category, Address
from django.conf import settings
from .errors import InvalidUsernamePassword, SessionAlreadyExpired, DeviceDataNotValid, UserDataNotValid, \
    CategoryDataNotValid, CategoriesNotFound, AddressDataNotValid, UserHasNoCategory, \
    UserHasNoAddress
from .utils import response, send_verification_email


class User(APIView):

    # @permission_classes([ApiTokenPermission])
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

    @permission_classes([ApiTokenPermission, LoggedInPermission, SessionExpiredPermission])
    @error_handler
    def get(self, request):
        return response(request.user.serialize())

    @permission_classes([ApiTokenPermission, LoggedInPermission, SessionExpiredPermission])
    @error_handler
    def delete(self, request):
        user = request.user
        session = Session.objects.get(token=request.user.session)
        session.expire_all_sessions()
        user.is_active = False
        user.save()
        return response()

    @permission_classes([ApiTokenPermission, LoggedInPermission, SessionExpiredPermission])
    @error_handler
    def patch(self, request):
        pass


class Login(APIView):
    # permission_classes = [ApiTokenPermission]

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
                if not user.is_verified:
                    send_verification_email(email)
                    return response(data={"email_check": "Please check your email to verify account"})
                login(request, user)
                session = Session(user=user, device_brand=session_data.validated_data.get('device_brand'),
                                  os_system=session_data.validated_data.get('os_system'))
                session.save()
                data = user.serialize()
                data["session_token"] = session.token
                return response(data=data)
            raise InvalidUsernamePassword()


class Logout(APIView):
    # # ApiTokenPermission
    permission_classes = [LoggedInPermission, SessionExpiredPermission]

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
            address = Address.objects.get(hash=data.get_hash())
            if address is None:
                address = data.create(data.validated_data)
            user.address = address
            user.save()
        raise AddressDataNotValid()

    @error_handler
    def get(self, request):
        user = request.user
        address = User.objects.get(user=user).address
        if address is not None:
            return response(data=address.serialize())
        raise UserHasNoAddress()

    def delete(self, request):
        pass