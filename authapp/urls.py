from django.urls import path
from authapp.views import UserRegister

app_name = 'authapp'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
]
