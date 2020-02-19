from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.views import obtain_auth_token

from . import views
from .views import User
from django.urls import path

urlpatterns = [
    path('user/', views.User.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('verify/', views.verify)
]
