from django.urls import path
from authapp.views import UserRegister, UserLogin

app_name = 'authapp'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
]
