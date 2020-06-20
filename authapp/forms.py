import hashlib
import random
from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm, PasswordChangeForm,
    SetPasswordForm
)
from authapp.models import User, UserVerify, UserProfile


class UserRegisterForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat your password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('name', 'email')

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label  # Add placeholder in input

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if not password1 or not password2 or password1 != password2:
            raise forms.ValidationError("Passwords don't match.")

        return password2

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already used.")
        return email

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()

        #  Verification by email
        user_verify = UserVerify()
        user_verify.user = user
        salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
        user_verify.verification_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
        user_verify.save()
        return user


class UserLoginForm(AuthenticationForm):

    class Meta:
        model = User
        fields = ('username', 'password')

    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class UserEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('email', 'name')

    def __init__(self, *args, **kwargs):
        super(UserEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
        self.fields['email'].widget.attrs['readonly'] = True
        self.fields['email'].widget.attrs['class'] = 'change-cursor'


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        fields = ('surname', 'country', 'city')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class ChangePasswordForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label


class PasswordConfirmForm(SetPasswordForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['placeholder'] = field.label
