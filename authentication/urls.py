from . import views
from django.urls import path

urlpatterns = [
    path('user/', views.User.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
    path('verify_email/', views.EmailVerification.as_view()),
    path('user_categories/', views.UserCategory.as_view()),
    path('user_addresses/', views.UserAddress.as_view()),
    path('categories/', views.get_all_categories),
]
