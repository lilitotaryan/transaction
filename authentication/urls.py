from . import views
from django.urls import path

urlpatterns = [
    path('signin/', views.Registration.as_view()),
    path('login/', views.login),
    path('logout/', views.logout),
]
