from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('add_account/', views.add_account, name='add_account'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('transfer/', views.transfer, name='transfer'),
    path('transaction_history/', views.transaction_history, name='transaction_history'),
]
