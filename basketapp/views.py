from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from mainapp.models import Languages
from basketapp.models import Basket


class BasketView(LoginRequiredMixin, View):
    template_name = 'basketapp/index.html'
    login_url = 'auth:login'

    def get(self, request):
        basket_items = Basket.objects.filter(user=request.user)

        context = {
            'title': 'Basket',
            'languages': Languages.get_languages(),
            'basket_items': basket_items,
        }
        return render(request, self.template_name, context)
