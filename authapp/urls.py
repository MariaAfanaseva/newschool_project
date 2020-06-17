from django.urls import path
from django.contrib.auth import views as auth_views
from authapp.views import (
    UserRegister, UserLogin,
    UserLogout, UserVerify,
    UserProfileView, ChangePasswordView
)

app_name = 'authapp'

urlpatterns = [
    path('register/', UserRegister.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', UserLogout.as_view(), name='logout'),
    path('verify/<email>/<verification_key>/', UserVerify.as_view(),
         name='verify'),
    path('profile/', UserProfileView.as_view(), name='profile'),

    path('password_change/', ChangePasswordView.as_view(),
         name='password_change'),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='authapp/password_done.html'),
         name='password_change_done'),

]
