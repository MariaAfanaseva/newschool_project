from django.shortcuts import render
from authapp.forms import UserRegisterForm
from django.views import View


class UserRegister(View):
    def get(self, request):
        register_form = UserRegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, 'authapp/register.html', context)

    def post(self, request):
        register_form = UserRegisterForm(request.POST)
        if register_form.is_valid():
            register_form.save()
            return render(request, 'authapp/verification.html')
        return self.get(request)
