import logging
from django.shortcuts import render, HttpResponseRedirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import (
    PasswordChangeView, PasswordResetView,
    PasswordResetConfirmView
)
from django.urls import reverse_lazy
from authapp.forms import (
    UserRegisterForm, UserLoginForm,
    UserEditForm, UserProfileForm,
    ChangePasswordForm, PasswordConfirmForm
)
from school.settings import DOMAIN_NAME, EMAIL_HOST_USER
from authapp.models import User


logger = logging.getLogger(__name__)


class UserRegister(View):
    template_name = 'authapp/register.html'
    template_verify = 'authapp/verification.html'
    register_form = UserRegisterForm

    @staticmethod
    def _send_verify_mail(user):
        verify_link = reverse('auth:verify', kwargs={'email': user.email,
                                                     'verification_key': user.userverify.verification_key})
        title = f'Account Verification {user.email}'
        message = f'To confirm your account {user.email} on the portal ' \
            f'{DOMAIN_NAME} follow the link: {DOMAIN_NAME}{verify_link}'
        return send_mail(title, message, EMAIL_HOST_USER, [user.email], fail_silently=False)

    def get(self, request):
        register_form = self.register_form()
        context = {
            'title': 'Registration',
            'register_form': register_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        register_form = self.register_form(request.POST)
        if register_form.is_valid():
            new_user = register_form.save()
            if self._send_verify_mail(new_user):
                return render(request, self.template_verify)
        return render(request, self.template_name, {'register_form': register_form})


class UserLogin(View):
    template_name = 'authapp/login.html'
    login_form = UserLoginForm

    def get(self, request):
        login_form = self.login_form()
        next_url = request.GET['next'] if 'next' in request.GET.keys() else ''
        context = {
            'title': 'Login',
            'login_form': login_form,
            'next': next_url,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        login_form = self.login_form(request, data=request.POST)
        if login_form.is_valid():
            user = authenticate(
                request,
                username=login_form.cleaned_data.get('username'),
                password=login_form.cleaned_data.get('password')
            )

            if user and user.is_active:
                login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))

        return render(request, self.template_name, {'login_form': login_form})


class UserLogout(LoginRequiredMixin, View):
    login_url = 'auth:login'

    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('main:index'))


class UserVerify(View):
    template_name = 'authapp/verification.html'

    def get(self, request, email, verification_key):
        context = {
            'title': 'Verification',
        }
        user = User.objects.get(email=email)
        if user.userverify.verification_key == verification_key and \
                user.userverify.is_verification_key_valid():
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, self.template_name, context)
        else:
            logger.error('User dose not verify by verify link.')
            return render(request, self.template_name, context)


class UserProfileView(LoginRequiredMixin, View):
    login_url = 'auth:login'
    template_name = 'authapp/profile.html'
    edit_form = UserEditForm
    profile_form = UserProfileForm

    def get(self, request):
        next_url = request.GET['next'] if 'next' in request.GET.keys() else ''
        user_form = self.edit_form(instance=request.user)
        profile_form = self.profile_form(instance=request.user.userprofile)
        context = {
            'title': 'Profile',
            'user_form': user_form,
            'profile_form': profile_form,
            'next': next_url,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        user_form = self.edit_form(request.POST, instance=request.user)
        profile_form = self.profile_form(request.POST, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()  # signal from user save user profile
            print(request.POST.keys())
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('main:index'))

        return render(request, self.template_name,
                      {'user_form': user_form, 'profile_form': profile_form})


class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = 'authapp/password_change.html'
    success_url = reverse_lazy('auth:password_change_done')


class ResetPasswordView(PasswordResetView):
    template_name = 'authapp/password_reset.html'
    success_url = reverse_lazy('auth:password_reset_done')
    subject_template_name = 'authapp/password_reset_subject.txt'
    email_template_name = 'authapp/password_reset_email.html'


class ResetPasswordConfirmView(PasswordResetConfirmView):
    form_class = PasswordConfirmForm
    template_name = 'authapp/password_reset_confirm.html'
    success_url = reverse_lazy('auth:password_reset_complete')
