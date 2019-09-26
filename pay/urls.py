from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.Transaction.as_view()),
]
