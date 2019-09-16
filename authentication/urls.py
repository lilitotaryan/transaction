from . import views
from django.urls import path

urlpatterns = [
    path('regestration/', views.regestration),
    path('login/', views.login),
    path('logout/', views.logout),
    path('moneytransaction/', views.MoneyTransaction.as_view()),
    path('bonustransaction/', views.bonus_transaction),
]
