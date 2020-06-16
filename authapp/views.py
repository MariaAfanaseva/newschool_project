from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import send_mail
from authapp.forms import UserRegisterForm, UserLoginForm
from school.settings import DOMAIN_NAME, EMAIL_HOST_USER
from authapp.models import User


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={'email': user.email,
                                                 'verification_key': user.userverify.verification_key})
    title = f'Account Verification {user.email}'
    message = f'To confirm your account {user.email} on the portal ' \
        f'{DOMAIN_NAME} follow the link: {DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, EMAIL_HOST_USER, [user.email], fail_silently=False)


class UserRegister(View):

    def get(self, request):
        register_form = UserRegisterForm()
        context = {
            'title': 'Registration',
            'register_form': register_form,
        }
        return render(request, 'authapp/register.html', context)

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            if send_verify_mail(new_user):
                return render(request, 'authapp/verification.html')
        return render(request, 'authapp/register.html', {'register_form': register_form})


class UserLogin(View):

    def get(self, request):
        login_form = UserLoginForm()
        context = {
            'title': 'Login',
            'login_form': login_form,
        }
        return render(request, 'authapp/login.html', context)

    def post(self, request):
        login_form = UserLoginForm(request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(
                request,
                username=login_form.cleaned_data.get('username'),
                password=login_form.cleaned_data.get('password')
            )

            if user and user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('main:index'))

        return render(request, 'authapp/login.html', {'login_form': login_form})


class UserLogout(View):

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main:index'))


class UserVerify(View):

    def get(self, request, email, verification_key):
        user = User.objects.get(email=email)
        if user.userverify.verification_key == verification_key and \
                user.userverify.is_verification_key_valid():
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            return render(request, 'authapp/verification.html')
