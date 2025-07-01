from django.contrib import admin
from django.urls import path, include
from myWalletapp.views import signup
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', signup, name='signup'), 
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('myWalletapp.urls')),
]