from . import views
from django.urls import path

urlpatterns = [
    # path('signup/', views.Registration.as_view()),
    path('login/', views.Login.as_view()),
    path('logout/', views.Logout.as_view()),
]
