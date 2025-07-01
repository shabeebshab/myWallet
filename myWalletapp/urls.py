from django.urls import path, include
from . import views
from myWalletapp.views import signup 

app_name = 'myWalletapp'

urlpatterns = [
    path('', views.wallet_view, name='wallet'),
    path('add-income/', views.add_transaction, {'transaction_type': 'IN'}, name='add_income'),
    path('add-expense/', views.add_transaction, {'transaction_type': 'EX'}, name='add_expense'),
    path('add-category/', views.add_category, name='add_category'), 
    path('accounts/signup/', signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('transactions/', views.transaction_list, name='transaction_list'),
    path('credits/', views.credit_view, name='credit_view'),
    path('mark-returned/<int:pk>/', views.mark_as_returned, name='mark_as_returned'),


   
]