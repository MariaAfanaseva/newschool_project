from django.urls import path
from authapp.views import (UserRegister, UserLogin,
                           UserLogout, UserVerify,
                           UserProfileView)

app_name = 'authapp'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('verify/<email>/<verification_key>/', UserVerify.as_view(),
         name='verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]
