from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login
from django.urls import reverse
from authapp.forms import UserRegisterForm, UserLoginForm


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
            register_form.save()
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
